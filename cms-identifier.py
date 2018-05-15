import requests, re, sys, time
from bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool


def joomla_identifier(url):
       isJoomla = "False"
       req = requests.get(url)
       soup = BeautifulSoup(req.text, 'lxml')
       meta = soup.find_all("meta")
       if  "joomla" in str(meta).lower():
            isJoomla = "True"
       else:
            admin = requests.get(url+"/administrator")
            if "Username" in admin.text:
                 isJoomla = "True"
            else: 
                 robots = requests.get(url+"/robots.txt")
                 if robots.text.find("joomla") != -1:
                      isJoomla = "True"
                 else:
                      pass
       return isJoomla  

def wordpress_identifier(url):
       isWordpress = "False"
       req = requests.get(url)
       soup = BeautifulSoup(req.text, 'lxml')
       meta = soup.find_all("meta")
       if  "wordpress" in str(meta).lower():
            isWordpress = "True"
       else:
            robots = requests.get(url+"/robots.txt")
            if robots.text.find("wp-") != -1:
                 isWordpress = "True"
            else:
                 pass
       return isWordpress  


def search_for(url):
            dicos = {"joomla": [], "wordpress": []}
            try:
                if joomla_identifier(url) == "True":
                      dicos['joomla'].append(url)
                elif wordpress_identifier(url) == "True":
                      dicos['wordpress'].append(url)
            except:
                      pass
            return dicos


def printf(lista): 
      for i in lista:
            link = str(i)
            ch = link.replace("%3F", "?")
            ch2 = ch.replace("%3D","=")
            print(ch2 )

"""def export_to_txt(urls):
  with open('file.txt','w') as file:
      for item in urls:
          print>>file, item"""



def main():
      proc    = int( sys.argv[1]  )
      start_time = time.time()
      result = {'joomla': [], 'wordpress': []}
      p = Pool(proc) 
      q = Pool(proc)
      f = open("file.txt")
      lines = f.readlines()
      all = p.map(search_for, lines)
      for p in all:
         if p.get("joomla") != []:
            result["joomla"].append(p.get("joomla"))
         elif p.get("wordpress") != []:
            result["wordpress"].append(p.get("wordpress"))

      print "#################################################"
      print( " Number of charged urls : " + str( len( lines ) ) )
      print "#################################################"
      print( " Number of joomla urls : " + str( len( result["joomla"] ) ) )
      print( " Number of wordpress urls : " + str( len( result["wordpress"] ) ) )
      print( " Finished in : " + str( int( time.time() - start_time ) ) + "s")
      print "#################################################" 
      print "Joomla links"
      print "#################################################" 
      for item in result["joomla"]:
            printf(item)
      print "#################################################" 
      print "Wordpress links"
      print "#################################################" 
      for item in result["wordpress"]:
            printf(item)

if __name__ == '__main__':
      main()
