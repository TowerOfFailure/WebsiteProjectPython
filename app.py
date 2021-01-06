from flask import Flask,redirect,request,url_for
from flask import render_template
from flask_bootstrap import Bootstrap
import pandas as pd


#Loading the jupyter notebook
import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.enable_gui=lambda x,y:False

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path

class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print ("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)


        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
          for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = self.shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in themodule
                exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod

sys.meta_path.append(NotebookFinder())
import import_ipynb
import Website_final_project_AI

#The Flask application

app=Flask(__name__,template_folder="Templates")
Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def welcome():
	if request.method =="POST":
		name=request.form.get("indiv_name")
		return redirect("name/"+name)
	return render_template('InputsTest.html')

@app.route('/name/<string:name>/')
def welcome2(name):
	return render_template('index.html',name=name)

@app.route('/infos1/',methods=['GET','POST'])
def dataHW():
	if request.method =="POST":
		height=float(request.form.get("height"))/100
		weight=float(request.form.get("weight"))
		MBI=weight/height**2
		classification=result(MBI)
		return render_template('resultMBI.html',result="Your MBI is of : "+str(MBI),meaning="This means that you are : "+classification)
	return render_template('InputsHW.html')

@app.route('/infos2/',methods=['GET','POST'])
def dataAI1():
	if request.method =="POST":
		Age=float(request.form.get("Age"))
		history=(request.form.get("History")=="on")*"yes"+"no"*(request.form.get("History")!="on")
		gender = request.form.get("Gender")
		favc=(request.form.get("Calory")=="on")*"yes"+"no"*(request.form.get("Calory")!="on")
		fcvc=float(request.form.get("Veggies"))
		ncp=float(request.form.get("Nmeals"))
		caec=request.form.get("Picking")
		smoke=(request.form.get("Smoke")=="on")*"yes"+"no"*(request.form.get("Smoke")!="on")
		water= float(request.form.get("Water"))
		scc=(request.form.get("Monitoring")=="on")*"yes"+"no"*(request.form.get("Monitoring")!="on")
		faf=float(request.form.get("Activity"))
		tue=float(request.form.get("Tech"))
		alcohol=request.form.get("Alcohol")
		transport=request.form.get("transportation")
		person=pd.DataFrame([[gender,Age,history,favc,fcvc,ncp,caec,smoke,water,scc,faf,tue,alcohol,transport]],columns=["Gender","Age","family_history_with_overweight","FAVC","FCVC","NCP","CAEC","SMOKE","CH2O","SCC","FAF","TUE","CALC","MTRANS"])
		classification=Website_final_project_AI.applyModel1(person)
		return render_template('resultAI.html',meaning="The AI thinks that you are : "+str(classification))
	return render_template('InputsAI.html')

@app.route('/infos3/',methods=['GET','POST'])
def dataAI2():
	if request.method =="POST":
		Age=float(request.form.get("Age"))
		history=(request.form.get("History")=="on")*"yes"+"no"*(request.form.get("History")!="on")
		gender = request.form.get("Gender")
		favc=(request.form.get("Calory")=="on")*"yes"+"no"*(request.form.get("Calory")!="on")
		fcvc=float(request.form.get("Veggies"))
		ncp=float(request.form.get("Nmeals"))
		caec=request.form.get("Picking")
		smoke=(request.form.get("Smoke")=="on")*"yes"+"no"*(request.form.get("Smoke")!="on")
		water= float(request.form.get("Water"))
		scc=(request.form.get("Monitoring")=="on")*"yes"+"no"*(request.form.get("Monitoring")!="on")
		faf=float(request.form.get("Activity"))
		tue=float(request.form.get("Tech"))
		alcohol=request.form.get("Alcohol")
		transport=request.form.get("transportation")
		person=pd.DataFrame([[gender,Age,history,favc,fcvc,ncp,caec,smoke,water,scc,faf,tue,alcohol,transport]],columns=["Gender","Age","family_history_with_overweight","FAVC","FCVC","NCP","CAEC","SMOKE","CH2O","SCC","FAF","TUE","CALC","MTRANS"])
		classification=Website_final_project_AI.applyModel2(person)
		return render_template('resultAI.html',meaning="The AI thinks that you are : "+str(classification))
	return render_template('InputsAI.html')

def result(MBI):
	if MBI<18.5:
		return "Underweight"
	elif MBI<25:
		return "Normal weight"
	elif MBI<30:
		return "Overweight"
	elif MBI<35:
		return "Obese level 1"
	elif MBI<40:
		return "Obese level 2"
	else:
		return "Obese level 3"


if __name__=="__main__":
	app.run(host="127.0.0.1",port=5000,debug=True)