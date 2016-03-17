# A python script that downloads all the pages from Mark Rosewater's tumblr and returns an XML
# document containing all the questions to which maro's answer contains some form of "maybe :)"
# A "maybe :)" is usually a form of precognition for magic related releases.
from lxml import etree
import os.path
from BeautifulSoup import BeautifulSoup
import urllib2
import re
def main():
    download_pages()
    parse_pages()
    
def download_pages():
	soup = BeautifulSoup(urllib2.urlopen('http://markrosewater.tumblr.com/page/1').read())
	num_pages = soup.findAll('span',attrs={'class':'page-number'})[0].getText().split("of")[1].strip()
	print(num_pages)
	for i in range(1,int(num_pages)):
		outfile = open("blogatog_page_" + str(i) + ".html", "w")
		print("Page: " + str(i))
		soup = BeautifulSoup(urllib2.urlopen('http://markrosewater.tumblr.com/page/' + str(i)).read())
		outfile.write(str(soup))
		outfile.close()
        
def parse_pages():
	blogfile = open("blogatog_page_1.html", "r")
	soup = BeautifulSoup(blogfile.read())
	menu = soup.findAll('div',attrs={'class':'post-content'})
	# some hackery to extract the number of pages to iterate through
	num_pages = int(soup.findAll('span',attrs={'class':'page-number'})[0].getText().split("of")[1].strip())
	print(str(num_pages) + "pages")
	outfile = open("_maybe_data.xml", "w", 0)
	convos = etree.Element("Conversations")
	question_counter = 0
    # parse pages till end
	for i in range(1,9000):
		blogfilename = "blogatog_page_" + str(i) + ".html"
		if not os.path.isfile(blogfilename):
			print ("no existy")
			break
		blogfile = open(blogfilename, "r")
		soup = BeautifulSoup(blogfile.read())
		# print(str(i))
		blogtxt = open(blogfilename, "r").read()
		page_soup = BeautifulSoup(blogtxt)
		menu = soup.findAll('div',attrs={'class':'post-content'})
		for subMenu in menu:
			if len(str(subMenu).split("</b></p><p>")) < 2:
				continue
            # hackery to split the question and answer
			q = str(subMenu).split("</b></p><p>")[0].split("asked: ")[1]
			a = str(subMenu).split("</b></p><p>")[1].replace("</p>\n</div>", "")
			a = html_escape(a)
            # regex to look for anything that looks like "maybe :)"
			if re.search("aybe.*:.*\)", a):
				q = BeautifulSoup(q).getText()
				a = BeautifulSoup(a.split("<div class=\"tags\">")[0]).getText()
				print q
				print a
				print("\n")
				# print("f")
				convo = etree.SubElement(convos, "Conversation")
				convo.set("id", str(question_counter))
				question_counter += 1
				etree.SubElement(convo, "Question").text = q
				etree.SubElement(convo, "Answer").text = a
	xmlout = etree.tostring(convos, pretty_print=True)
	outfile.write(xmlout)
    
class Conv(object):
	q = None	
	a = None

def html_escape(text):
	for i in range(6):
		text = text.replace("&amp;", "&")
		text = text.replace("&quot;", '"')
		text = text.replace("&apos;", "'")
		text = text.replace("&gt;", ">")
		text = text.replace("&lt;", "<")
		text = text.replace("&rsquo;", "'")
		text = text.replace("&ldquo;", '"')
		text = text.replace("&rdquo;", '"')
	return text
		
	
if __name__ == "__main__":
	main()