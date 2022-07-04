import sys
from os import path
import os
from datetime import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageCms
import configparser


config = configparser.ConfigParser()
config.read('constants.ini')

def getOption(option,number):
	return option.split('\n')[number].split(':')[1]
	
def getFontSize(name,size):
	namelength = len(name)
	if(size == 'xs'):
		if(namelength <= 7):
			return 800
		elif(namelength > 7 and namelength <= 9):
			return 720
		elif(namelength > 9 and namelength <= 11):
			return 600
		else:
			return 0
	elif(size == 's'):
		if(namelength <= 7):
			return 800
		elif(namelength > 7 and namelength <= 9):
			return 720
		elif(namelength > 9 and namelength <= 11):
			return 600
		else:
			return 0
	elif(size == 'm'):
		if(namelength <= 8):
			return 800
		elif(namelength > 8 and namelength <= 10):
			return 720
		elif(namelength > 10 and namelength <= 12):
			return 600
		else:
			return 0
	elif(size == 'l'):
		if(namelength <= 8):
			return 800
		elif(namelength > 8 and namelength <= 10):
			return 720
		elif(namelength > 10 and namelength <= 12):
			return 600
		else:
			return 0
	elif(size == 'xl'):
		if(namelength <= 9):
			return 800
		elif(namelength > 9 and namelength <= 11):
			return 720
		elif(namelength > 11 and namelength <= 13):
			return 600
		else:
			return 0
	elif(size == 'xxl'):
		if(namelength <= 9):
			return 800
		elif(namelength > 9 and namelength <= 11):
			return 720
		elif(namelength > 11 and namelength <= 13):
			return 600
		else:
			return 0
	


def getFrontTemplate(folder,design,color,size,name,number):
	path = design+'/'+color+ '/'+size 
	try:
		front = Image.open(path+ '-front.tif')
		new_front = front.copy()
		new_front.save(folder+'/'+design+'-'+color+'-'+size+'-'+'front'+'-'+name+'-'+number+'.tif',dpi=(300.0,300.0))
	except FileNotFoundError:
		print('Front file not found for ' + design + ' ' + color + ' ' + size + ':' + name + ' ' + number )
		return
	

def getSleeveTemplate(folder,design,color,size,sleeve,name,number,config_items):

	if(sleeve == 'half'):
		sleeveType = 'half'
	else:
		sleeveType = 'full'
	
	path = design+'/'+color+ '/'+sleeveType 

	sleevePattern = int(config_items['sleevePattern'])

	try:
		left = Image.open(path+ '-left.tif')
		new_left = left.copy()
		new_left.save(folder+'/'+design+'-'+color+'-'+size+'-'+sleeve+'-'+'left'+'-'+name+'-'+number+'.tif',dpi=(300.0,300.0))
	except FileNotFoundError:
		print('Left sleeve not found for ' + design + ' ' + color + ' ' + sleeveType)

	if(sleevePattern == 2):
		try:
			right = Image.open(path+ '-right.tif')
			new_right = right.copy()
			new_right.save(folder+'/'+design+'-'+color+'-'+size+'-'+sleeve+'-'+'right'+'-'+name+'-'+number+'.tif',dpi=(300.0,300.0))
		except FileNotFoundError:
			print('Right sleeve not found for ' + design + ' ' + color + ' ' + sleeveType)

def getCollarCuffTemplate(folder,design,color,size,name,number,config_items):
	if(config_items['collar']=='True'):
		try:
			path = design+'/'+color+ '/'
			collar = Image.open(path+ 'collar.tif')
			new_collar = collar.copy()
			new_collar.save(folder+'/'+design+'-'+color+'-'+size+'-'+name+'-'+number+'-collar.tif',dpi=(300.0,300.0))
		except:
			if color == 'white':
				return
			else:
				print('Collar not found for ' + design + ' ' + color )
				return
	if(config_items['cuff'] =='True'):
		try:
			path = design+'/'+color+ '/'
			cuff = Image.open(path+ 'cuff.tif')
			new_cuff = cuff.copy()
			new_cuff.save(folder+'/'+design+'-'+color+'-'+size+'-'+name+'-'+number+'-cuff(2 copies)'+'.tif',dpi=(300.0,300.0))
		except:
			print('Cuff not found for ' + design + ' ' + color )
			return
	

def getBackTemplate(folder,design,color,size,name,number,config_items):
	path = design+'/'+color +'/'+size
	try:
		back = Image.open(path+'-back.tif')
		drawbackFile(name,number,size,color,back,config_items)
		back.save(folder+'/'+design+'-'+color+'-'+size+'-'+'back'+'-'+name+'-'+number+'.tif',dpi=(300.0,300.0))
	except FileNotFoundError:
		print('Back file not found for ' + design + ' ' + color + ' ' + size + ':' + name + ' ' + number )
		return

def drawbackFile(name,number,size,color,image,config_items):
		fontsize = getFontSize(name,size)
		if(fontsize == 0):
			print('Name length exceeded maximum limit for customer : ' + name + ' ' + number)
			print('Skipping file generation...')
			print()
			return
		
		namefont = ImageFont.truetype("font-test.ttf", fontsize)
		numberfont= ImageFont.truetype("font-test.ttf", 4000)
		d = ImageDraw.Draw(image)
		c,m,y,k  = config_items[color].split(',')
		r = round(2.55*int(c))
		g = round(2.55*int(m))
		b = round(2.55*int(y))
		a = round(2.55*int(k))
		

		if(size == 'xs'):
			nameX = 3150
			nameY = 1430
			numberX = 3150
			numberY = 2860
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number), fill =(r,g,b,a), anchor="mt", font=numberfont)
		elif(size == 's'):
			nameX = 3300
			nameY = 1500
			numberX = 3300
			numberY = 3000
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number), fill =(r,g,b,a), anchor="mt", font=numberfont)
		elif(size == 'm'):
			nameX = 3450
			nameY = 1500
			numberX = 3450
			numberY = 2400
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number), fill =(r,g,b,a), anchor="mt", font=numberfont)
		elif(size == 'l'):
			nameX = 3600
			nameY = 1500
			numberX = 3600
			numberY = 2400
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number), fill =(r,g,b,a), anchor="mt", font=numberfont)
		elif(size == 'xl'):
			nameX = 3750
			nameY = 1500
			numberX = 3750
			numberY = 2400
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number),fill =(r,g,b,a), anchor="mt", font=numberfont)
		elif(size == 'xxl'):
			nameX = 3900
			nameY = 1500
			numberX = 3900
			numberY = 3000
			# d.text((nameX, nameY), name,fill =(r,g,b,a),font=namefont, anchor="mt")
			d.text((numberX, numberY), str(number), fill =(r,g,b,a), anchor="mt", font=numberfont)		

def generateFiles(filepath):

	excelData  = pd.read_excel(filepath,header = 1,usecols=["order_number","name","options"])
	data = excelData.to_dict("records")

	today = datetime.now()

	folder = today.strftime('%Y%m%d')
	os.mkdir(today.strftime('%Y%m%d'))

	for i in data:
		option = i["options"]
		
		design = i["name"].lower().split(' ')
		try:
			cIndex = design.index('custom')
			design = ''.join(design[0:cIndex])
		except:
			design = ''.join(design)
		
		
		order_number = i["order_number"]
		name = getOption(option,4)
		number = getOption(option,5)
		color = getOption(option,0).lower().split(' ')
		color = ''.join(color)
		size = getOption(option,3).split(' ')[0].lower()
		sleeve = getOption(option,2).lower()

		print()
		print('Order : ' + '#'+ order_number +' | ' + 'Name : ' + name)


		try:
			config_items = config[design]
			getFrontTemplate(folder,design,color,size,name,number)
			getSleeveTemplate(folder,design,color,size,sleeve,name,number,config_items)
			getBackTemplate(folder,design,color,size,name,number,config_items)
			getCollarCuffTemplate(folder,design,color,size,name,number,config_items)
		except KeyError:
			print(design + ' not available!')
			print('Skipping file generation for customer: ' + name)
			continue
		print()

def generateCustomFiles(filepath):

	excelData  = pd.read_excel(filepath,header=1)
	data = excelData.to_dict("records")

	exceptions = 0	

	config_items = config['custom']
	outputpath = config['custom']['ordername']
	os.mkdir(outputpath)
	path = config['custom']['templatepath'] + '/'

	
	print()
	print('Store location : ' + outputpath )
	print('File generation started...')
	print()

	print('Printing collars and cuffs...')	
	if(config['custom']['collar'] == "True"):
		collar = Image.open(path+'collar.tif')
		collar.save(outputpath + '/'+ 'collar' + '('+ str(len(data)) + ' copies' +')'  +'.tif',dpi=(300.0,300.0))
		print('Saved ' + str(len(data))  +' copies of collar')
	
	if(config['custom']['cuff'] == "True"):
		cuff = Image.open(path+'cuff.tif')
		cuff.save(outputpath + '/'+ 'cuff' + '('+ str(len(data) *2) + ' copies' +')'  +'.tif',dpi=(300.0,300.0))
		print('Saved ' + str(len(data) *2)  +' copies of cuff')

	print()	

	for i in data:
		name = i['name']
		number =str(i['number']).split('.')[0]
		size  = i['size'].lower()
		sleeve = i['sleeve'].lower()
		
		print(number)
		print('Name : '+ name.upper())

		try:
			front = Image.open(path+size+'-front.tif')
			front.save(outputpath + '/' + size +'-front-'+ name+'-' +str(number) + '.tif',dpi=(300.0,300.0))
			print('Front printed...')
		except:
			exceptions = exceptions + 1
			print('------------------------------------------------')
			print("Front not found for size : " + size)
			print('------------------------------------------------')

		try:
			back = Image.open(path + size + '-back.tif')
			drawbackFile(name,number,size,'color',back,config_items)
			back.save(outputpath + '/' + size +'-back-'+ '-'+name+'-'+ str(number)+ '.tif')
			print('Back printed...')
		except:
			exceptions = exceptions + 1
			print('------------------------------------------------')
			print("Execption : Back not found for size :" + size)
			print('------------------------------------------------')

		try:
			left = Image.open(path+ sleeve+'-left.tif')
			new_left = left.copy()
			new_left.save(outputpath + '/' +sleeve+'-'+'left-'+ name+'-'+str(number)  +'.tif',dpi=(300.0,300.0))
			print('Left sleeve printed...')
		except FileNotFoundError:
			exceptions = exceptions + 1
			print('------------------------------------------------')
			print('Execption : Left sleeve not found')
			print('------------------------------------------------')

		
		if(config['custom']['sleevePattern'] == '2'):
			try:
				right = Image.open(path+sleeve+ '-right.tif')
				new_right = right.copy()
				new_right.save(outputpath + '/' +sleeve+'-'+'right-'+ name+'-'+str(number) +'.tif',dpi=(300.0,300.0))
				print('Right sleeve printed...')
			except FileNotFoundError:
				exceptions = exceptions + 1
				print('------------------------------------------------')
				print('Execption : Right sleeve not found')
				print('------------------------------------------------')

		print()	
	
	print('File generation complete.')
	print('Exceptions found : ' + str(exceptions) )
	print()



if len(sys.argv) != 3:
	print('Arguments missing...')
	print('command : python3 [filename] [regular/custom]')
else:
	if(sys.argv[2] == 'regular'):
		generateFiles(sys.argv[1])
	elif(sys.argv[2] == 'custom'):
		generateCustomFiles(sys.argv[1])