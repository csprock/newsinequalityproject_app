import psycopg2
import shapefile
import pandas as pd
import json
import numpy as np


###################################### gentrification articles by neighborhood ##############################
# gentrification articles by neighborhood along with "is gentrifying" according to Furman center

gent_info = pd.read_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/FurmanCenter_Gentrification.csv').fillna(0)
gent_info['Gentrifying'] = gent_info['Gentrifying'].apply(int)


query = '''
        CREATE TEMP VIEW gentrification AS SELECT COUNT(DISTINCT(tags.id)), article_selectors.nta_code, article_selectors.name FROM tags INNER JOIN article_selectors ON tags.id = article_selectors.id WHERE tags.keyword = 'Gentrification' GROUP BY article_selectors.nta_code, article_selectors.name;
        SELECT gentrification.count, sba_code, gentrification.nta_code, name FROM gentrification LEFT JOIN code_table ON gentrification.nta_code = code_table.nta_code;
        '''

temp = executeSQL_select(query, None, 'nyc_neighborhood_articles','redalert','postgres', column_names = ['counts','SBA','nta_code', 'nta_name'])

map_data = pd.merge(temp, gent_info, how = 'left', on = 'SBA').drop_duplicates()


reader = shapefile.Reader("C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/Geometry/NTA/NTA.shp")
fields = reader.fields[1:]
field_names = [f[0] for f in fields]
buffer = []

for sr in reader.shapeRecords():
    
    geo = sr.shape.__geo_interface__
    attr = dict(zip(field_names, sr.record))
    
    i = sr.record[2]
    if i in map_data['nta_code'].values:
        temp = map_data.loc[map_data['nta_code'] == i]
        attr['counts'] = int(temp.counts.values[0])
        attr['gent'] = int(temp.Gentrifying.values[0])
    else:
        attr['counts'] = 0
        attr['gent'] = 0
        
    
    buffer.append(dict(type="Feature", geometry = geo, properties = attr))


from json import dumps

geojson = open("C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/ByNeighborhood/gent_map.geojson","w")
geojson.write(dumps({"type":"FeatureCollection", "features":buffer}, indent = 2) + "\n")
geojson.close()



########################### by community district ####################################################
# gentrification articles by community district along with "is gentrifying" according to Furman center
query = '''
        CREATE TEMP VIEW gentrification AS SELECT COUNT(DISTINCT(tags.id)) AS count, article_selectors.nta_code FROM tags INNER JOIN article_selectors ON tags.id = article_selectors.id WHERE tags.keyword = 'Gentrification' GROUP BY article_selectors.nta_code;
        SELECT SUM(gentrification.count), boro_cd, sba_code FROM gentrification INNER JOIN code_table ON gentrification.nta_code = code_table.nta_code GROUP BY boro_cd, sba_code;
        '''
    
gent_articles = executeSQL_select(query, None,'nyc_neighborhood_articles', 'redalert','postgres', column_names = ['counts','boro_cd', 'SBA'])


map_data = pd.merge(gent_articles, gent_info, how = 'left', on = 'SBA').fillna(0).drop_duplicates()
map_data.index = map_data['boro_cd']
del map_data['boro_cd']


with open('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/Geometry/CD/Community_Districts.geojson') as f:
    cd_data = json.load(f)
    

for j, f in enumerate(cd_data['features']):
    
    i = int(f['properties']['boro_cd'])
    
    if i in map_data.index.values:
        temp = map_data.loc[i]
        cd_data['features'][j]['properties']['counts'] = int(temp.counts)
        cd_data['features'][j]['properties']['gent'] = int(temp.Gentrifying)
    else:
        cd_data['features'][j]['properties']['counts'] = 0
        cd_data['features'][j]['properties']['gent'] = 0
    

geojson = open("C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/ByDistrict/gent_map.geojson","w")
json.dump(cd_data, geojson)

geojson.close()


########################### gentrification articles / rent changes ################################
# gentrification articles and change in rents by community district

query = '''
        CREATE TEMP VIEW gentrification AS SELECT COUNT(DISTINCT(tags.id)) AS count, article_selectors.nta_code FROM tags INNER JOIN article_selectors ON tags.id = article_selectors.id WHERE tags.keyword = 'Gentrification' GROUP BY article_selectors.nta_code;
        SELECT SUM(gentrification.count), boro_cd, sba_code FROM gentrification INNER JOIN code_table ON gentrification.nta_code = code_table.nta_code GROUP BY boro_cd, sba_code;
        '''
    
gent_articles = executeSQL_select(query, None,'nyc_neighborhood_articles', 'redalert','postgres', column_names = ['counts','boro_cd', 'SBA'])

rentChanges = pd.read_csv("C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/rentChange.csv")


combined = pd.merge(rentChanges, gent_articles, how = 'left', on = 'SBA')[['CD_code','boro_cd_x','SBA','rentChange','counts']]
combined['counts'] = combined['counts'].fillna(0)
#combined['rentChange'] = combined['rentChange'].replace(np.nan, None)
combined.columns = ['cd_code','boro_cd','SBA','rentChange','articles']
combined.index = combined['boro_cd']
del combined['boro_cd']



combined = combined.groupby('boro_cd').agg({'rentChange':'mean','articles':'sum'})
combined['rentChange'] = combined['rentChange'].fillna(-1)

combined.to_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/articles_rents.csv')


with open('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/Geometry/CD/Community_Districts.geojson') as f:
    cd_data = json.load(f)
    

for j, f in enumerate(cd_data['features']):
    
    i = int(f['properties']['boro_cd'])
    
    if i in combined.index.values:
        temp = combined.loc[i]
        cd_data['features'][j]['properties']['counts'] = int(temp.articles)
        
        if temp.rentChange == -1:
            print("----")
            cd_data['features'][j]['properties']['rents'] = None
        else:
            cd_data['features'][j]['properties']['rents'] = temp.rentChange
        
    else:
        cd_data['features'][j]['properties']['counts'] = None
        cd_data['features'][j]['properties']['rents'] = None
    

geojson = open("C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/withRent/gent_map.geojson","w")
json.dump(cd_data, geojson)
geojson.close() 




################################### scatter plot ################################################

article_rent = pd.read_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Data/articles_rents.csv', sep = ",")

codes = executeSQL_select("SELECT nta_code, boro_cd, cd_name FROM code_table;", None, 'nyc_neighborhood_articles','redalert','postgres', column_names = ['nta_code','boro_cd', 'cd_name'])
link_data = executeSQL_select("SELECT nta_code, borough FROM neighborhood;", None, 'nyc_neighborhood_articles','redalert','postgres', column_names = ['nta_code','boro_name'])

codes = pd.merge(codes, link_data, on = 'nta_code', how = 'left')[['boro_cd','cd_name','boro_name']].drop_duplicates()

combined = pd.merge(article_rent, codes, on = 'boro_cd', how = 'inner')

combined.to_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/scatter_plot/rent_scatter.csv')




###################### number of articles per year #############################################

query = "SELECT COUNT(id), date_part('year', date) FROM tags WHERE keyword = 'Gentrification' GROUP BY date_part('year', date)"
results = executeSQL_select(query, None, 'nyc_neighborhood_articles','redalert','postgres')
results[1] = results[1].apply(int)
results.columns = ['articles','date']

new_data = pd.Series({'articles':0, 'date':2009})

results = results.append(new_data, ignore_index = True)


results = results.sort_values(by = 'date',axis = 0)

results.to_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/gent_counts.csv')


######################## number of articles by borough ########################################
# for bar chart of number of gentrification by borough
query = "SELECT borough, COUNT(DISTINCT(id)) FROM article_selectors WHERE id IN (SELECT id FROM tags WHERE keyword = 'Gentrification') GROUP BY borough;"
results = executeSQL_select(query, None, 'nyc_neighborhood_articles', 'redalert', 'postgres')
results.columns = ['borough', 'articles']

results.to_csv('C:/Users/csprock/Documents/Projects/Data Journalism/News Inequality/Visualizations/gentrification/boro_counts.csv')





#################################################################################################
#connect to PostgreSQL database, returns connection object if successful, otherwise prints error
def connectToDatabase(dbname, psswrd, user, success_message = True):
    conn_string = "host='localhost' dbname='%s' user='%s' password='%s'" % (dbname, user, psswrd)
    
    try:
        conn = psycopg2.connect(conn_string)
        if success_message is True:
            print("Connected to database %s." % (dbname))
            
        return conn
    except:
        print('Error! Failure to connect to database %s' % (dbname))
        

# compact function for SQL SELECT query 
def executeSQL_select(query, tupl, dbname, psswrd, user, success_message = False, column_names = None):
    conn = connectToDatabase(dbname = dbname, psswrd = psswrd, user = user, success_message = success_message)
    cur = conn.cursor()
    if tupl is not None:
        cur.execute(query, tupl)
    else:
        cur.execute(query)
    results = cur.fetchall()
    cur.close
    conn.close
    if column_names is not None:
        results = pd.DataFrame(results, columns = column_names)
    else:
        results = pd.DataFrame(results)
    
    return results







