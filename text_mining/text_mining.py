"""
CITY SIMULARITY

created on Mon Feb 23 3:10:00 2015

@author: Michael Costello

"""
from pattern.web import *
import bs4
beautiful_soupy = bs4.BeautifulSoup #package that shit!

def get_city_text(city):
	""" taking an city name,
		output a text file containing the wikipedia article
	"""
	city_URL = 'http://en.wikipedia.org/wiki/' + city
	city_html = URL(city_URL).download()
	soup = beautiful_soupy(city_html)
	city_text = soup.get_text().encode('utf8')
	return city_text

def build_list(city):
	""" taking a text file for the wikipedia article of a city,
		output a list of all the unique words in the article
	"""
	city_text = get_city_text(city)
	city_list = []
	city_text = city_text.split( )
	bad_chars = '(){}[]".,1234567890 '

	for word in city_text:
		word = word.strip(bad_chars)
		if word not in city_list:
			city_list.append(word)
	return city_list

def compare_lists(city_1_list,city_2_list):
	""" taking in the dictionaries of each city article,
		outputs a new dictionary containing only the words present in
		both city articles
	"""
	same_list = []
	for word in city_1_list:
		if word in city_2_list:
			same_list.append(word)
	return len(same_list)

def compare_cities(city_1,city_2):
	""" taking the names of two cities for comparison,
		outputs the similarity percentage between the two cities
	"""
	len_same = compare_lists(build_list(city_1),build_list(city_2))
	avglen = (len(build_list(city_2))+len(build_list(city_1))) / 2
	ratio = len_same/(avglen+0.0)
	return ratio

def main():
	city_1 = raw_input("First city: ")
	city_2 = raw_input("Second city: ")
	ratio = compare_cities(city_1,city_2)
	print "ratio is ", ratio
	if ratio >= 0.8:
		print "These cities are very similar"
	elif ratio >= 0.5:
		print "These cities are fairly similar"
	elif ratio >= 0.35:
		print "These cities are somewhat similar"
	else:
		print "These cities are not very similar"

if __name__ =='__main__':
	main()	