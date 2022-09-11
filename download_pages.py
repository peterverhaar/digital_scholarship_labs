import requests
import re
from bs4 import BeautifulSoup
import os

from os.path import exists


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context




output_dir = 'Webpages'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


log = open('log.txt' , 'a', encoding = 'utf-8')

labs_urls = []

with open( 'lab_urls.txt' , encoding = 'utf-8' ) as labs_file:
    labs_urls = labs_file.readlines()


for homepage in labs_urls:

    homepage = homepage.strip()
    print('Lab homepage: ' + homepage)

    dir_name = re.sub( r'https?:\/\/' , '' , homepage )
    if re.search( r'[/]' , dir_name):
        dir_name = dir_name[:dir_name.index('/')]

    dir_name = os.path.join( output_dir , dir_name)
    print(dir_name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)



    try:
        response = requests.get( homepage )
        if response:
            path = os.path.join( dir_name , 'index.html' )
            out = open( path , 'w' , encoding = 'utf-8' )

            html = response.text
            out.write(html)
            log.write( f'{homepage} downloaded successfully \n')
            print( f'{homepage} downloaded successfully')
            out.close()

            soup = BeautifulSoup( response.text , 'html.parser')
            links = soup.find_all("a")

            subpages = []

            for l in links:
                linktext = l.string
                url = l.get("href")
                if not( re.search( '^#' , str(url) ) ) and not( re.search( '^mailto' , str(url) ) ) and url is not None:
                    subpages.append( url )

            for url in subpages:
                print('URL: ' + url)
                if not(re.search( '(^http)|(^#)|(^mail)' , str(url) ) ):
                    if not( re.search( r'^[/]' , str(url) ) ):
                        url = '/' + url
                    url = homepage + url

                url = re.sub( r'[/]$' , '' , url  )
                file_name = os.path.basename(url)
                if not( re.search( r'[.]' , file_name) ):
                    file_name = file_name + '.html'
                file_name = re.sub( r'[/]' , '_'  , file_name )
                file_name = os.path.join( dir_name , file_name )


                print('Filename: ' + file_name)
                try:
                    if not( re.search( r'myendnoteweb' , url , re.IGNORECASE) ):
                        response = requests.get(url)
                        if response:
                            out = open( file_name , 'w' , encoding = 'utf-8' )
                            out.write(response.text)
                            out.close()
                            print(f"{url} downloaded succesfully")
                            log.write(f"{url} downloaded succesfully \n")
                except:
                    print(f'{url} cannot be downloaded.')

                if not( exists(file_name) ):
                    log.write( f'{url} not downloaded \n' )

    except:
        print( f'Problem with {homepage}')
        log.write( f'Problem with {homepage}\n')




log.close()
