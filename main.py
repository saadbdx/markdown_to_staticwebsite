import argparse
from pathlib import Path
import markdown2
import os
import shutil

#getArg function is used for getting command line arguments 
def getArg() :
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="Input path ", type=str)
	parser.add_argument("-o", help="Output path ", type=str)
	parser.add_argument("-t", help="Template path", type=str)
	parser.add_argument("-v", help="Verbose mode.", action="store_true")
	return parser.parse_args()

#printInfo is used to print information
def printInfo() :
    args = getArg()
    if args.i != None:
        print("The input path : ", args.i)
    else :
        print("Unknown input path")
    if args.o != None:
        print("The output path : ", args.o)
    else :
        print("Unknown output path")
    if args.t != None:
        print("The template path: ", args.t)
    else :
        print("Unknown template path")

#The main function
def main():
	
	#Store command line arguments in args
	args = getArg()
	
	#Print information to the user (verbose mode)
	if args.v:
	    printInfo()

    #Translate function 
	if args.i != None and args.o != None:
		traslate_Markdown_to_Html(args)
	else :
		print("incomplete request, please provide the missing information")

#To edit image line	
def add_image(html):

    args = getArg()

    out_path = Path(args.o + "/src")

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    result_string = ""
    for line in html.split("\n"):

        line = str(line)
        
        if "<img " in line:

            image_path = line.split('src="')[1].split('"')[0].split("/")[1]

            if args.v:
                print("image_path", image_path)

            shutil.copyfile(
                str(image_path), str(out_path) + "/" + image_path
            )
            line = (
                line.split('src="')[0]
                + 'src="./src/'
                + image_path
                + '" '
                +'height="500" width="500" '
                +'class="center" '
                + '/></p>'
            )
            result_string += "<center>" + line + "</center>" + "\n"          
        else:
            result_string += line + "\n"

    return result_string

#To translate markdawn file to html
def traslate_Markdown_to_Html(args) :
		
		#Open the mackdown file to translate
        with open(args.i, "r") as input_file:
            if args.v:
                print("Input file :", input_file.name)

            file_name = (
                 input_file.name.split("/")[1]
                 .split(".")[0]
            )

			#Open the html file
            with open(
                str(args.o) + "/" + str(file_name) + ".html", "w"
            ) as output_file:
                if args.v:
                    print("output file :", output_file.name)

                html = markdown2.markdown(input_file.read())

				#Check the template
                if args.t != None:
                    with open(args.t, "r") as template_file:
                        result = template_file.read().replace("main",html)
                else:
                    result = html
                
                result = add_image(result)

                output_file.write(result)
                     
#Call main function
main()
