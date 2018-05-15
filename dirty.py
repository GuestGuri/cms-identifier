import requests, re, sys, time
from bs4 import BeautifulSoup
from functools import partial
from multiprocess import Pool, TimeoutError, cpu_count



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


def search_for(urls):

        joomla = []
        wordpress = []
        for url in urls:
            try:
                if joomla_identifier(url) == "True":
                      joomla.append(url)
                elif wordpress_identifier(url) == "True":
                      wordpress.append(url)
                else:
                      pass
            except:
                print "flag"
        return joomla, wordpress


def printf(lista): 
      for i in lista:
            link = str(i)
            ch = link.replace("%3F", "?")
            ch2 = ch.replace("%3D","=")
            print( " " + ch2 )

"""def export_to_txt(urls):
  with open('file.txt','w') as file:
      for item in urls:
          print>>file, item"""



def main():
      #proc    = int( sys.argv[1]  )
      start_time = time.time()
      #result = []
      #p = Pool(proc) 
      f = open("file.txt")
      lines = f.readlines()
      #request = partial( search_for, string )
      #all = p.map(search_for, lines)

      #for p in all:
            #result += [ u for u in p]
            #printf( set( result ) )
      joomla, wordpress = search_for(lines)
      print "#################################################"
      print( " Number of charged urls : " + str( len( lines ) ) )
      print "#################################################"
      print( " Number of joomla urls : " + str( len( joomla ) ) )
      print( " Number of wordpress urls : " + str( len( wordpress ) ) )
      print( " Finished in : " + str( int( time.time() - start_time ) ) + "s")
      print "################################################# \n" 
      print "Joomla links \n"
      for item in joomla:
            print item
      print "Wordpress links \n"
      for item in wordpress:
            print item


if __name__ == '__main__':
      main()
