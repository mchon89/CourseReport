#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ----------------------------------------------
# course report.py 
# ----------------------------------------------


from bs4 import BeautifulSoup
import requests


if __name__ == "__main__":

# ---------------------------------------------- 
# First, we need to get the list of schools 
# and need to go to 
# https://www.coursereport.com/schools/eachschool
# for each school 
# ----------------------------------------------

	start_url = 'https://www.coursereport.com/schools?'
	base_url = 'https://www.coursereport.com/'
	tail_url = 'page='

	with open('course_report1.csv', 'w') as f:
		f.write('school' + ',' + 'school url' + ',' + 'location' + ',' + 'course name' + ',' + 'price' + ','
				+ 'skill' + ',' + 'description' + '\n')

# ---------------------------------------------- 
# there are 17 pages of bootcamp schools 
# ---------------------------------------------- 

		for i in range(1,18):
			url = start_url + tail_url + str(i)
			response = requests.get(url).content.decode()
			soup = BeautifulSoup(response, 'lxml')

# ---------------------------------------------- 
# getting the school name and url using 
# beautiful soup 
# ---------------------------------------------- 

			for school in soup.find_all('li', class_ = 'school-li'):
				school_name = school.a.get_text()
				school_url = school.a.get('href')

# ---------------------------------------------- 
# https://www.coursereport.com/schools/eachschool
# ---------------------------------------------- 

				another_url = base_url + school_url
				another_response = requests.get(another_url).content.decode()
				another_soup = BeautifulSoup(another_response, 'lxml')

# ----------------------------------------------
# looping over the campuses in each school
# => looping over a tag where I can get the info 
# regarding each school => loopin over each course
# in the tag 
# parsing the info using BeautifulSoup
# location, course name, price, skill, description
# ----------------------------------------------

				for campus in another_soup.find_all('div', class_ = 'campus panel panel-cr'):
					location = campus.find('div', class_ = 'col-lg-8 col-xs-12').get_text()
				
					for course in campus.find_all('div', class_ = 'panel panel-cr panel-cr-expandable'):
						try:
							course_name = course.find('div', class_ = 'col-sm-4 col-xs-12 course-name').get_text()
							course_name = course_name.strip().replace(',', ' ')
							course_name = course_name.strip().replace(':', ' ')
							
							course_price = course.find('span', class_ = 'price').get_text()
							course_price = course_price.strip().replace(',', ' ')
							
							course_skill = course.find('span', class_ = 'focus').get_text()
							course_skill = course_skill.strip().replace('\n', ' ')
							course_skill = course_skill.strip().replace('\r', ' ')
							course_skill = course_skill.strip().replace(',', ' ')

							course_desc = course.find('p').get_text()
							course_desc = course_desc.strip().replace('\n', ' ')
							course_desc = course_desc.strip().replace('\r', ' ')
							course_desc = course_desc.strip().replace(',', ' ')

						except:
							pass

# ----------------------------------------------
# writing the appropriate features 
# ----------------------------------------------

						f.write(school_name + ',' + school_url + ',' + location + ',' + course_name + ',' + course_price + ',' 
								+ course_skill + ',' + course_desc + '\n')


