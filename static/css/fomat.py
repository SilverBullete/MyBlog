css = open("notion.css", "r", encoding="utf-8")
new_css = open("new_notion.css", "w")
txt = ""
index = 1
for line in css.readlines():
    if line.find("	")==0 or line.find("}")==0 or line=="\n":
        txt += line
    else:
        txt += ".blog-content " + line
    print(line, line=='\n')
new_css.write(txt)
css.close()
new_css.close()