

# Why is this interesting? #

What this demonstrates is that this library is capable of accomplishing the following things:

  1. Combining XML schemas from different projects
  1. Compiling those schemas in to java objects
  1. Combining the java objects with a networking library and with a graph library
  1. Making the java objects available via Jython to a Python scripting environment

As additional XML schemas from around Neuroinformatics are added, their basic types can be made accessible as well, which means that scripts can be written that take information out of one data type and put them into another.

# An example usage #

This example downloads a set of NeuroML files from the Whole Brain Catalog server, processes them in memory to extract their endpoints, spits the results out in a Python file, and then enables those results to be computed on using standard Python libraries.

# Getting started #

## Building from source ##

**NOTE**: If you want to skip this step, you can [download a pre-build jar from the downloads section.](http://code.google.com/p/incf-omni/downloads/list)

In order to be most general, OMNI takes advantage of libraries in both Python and Java.  Therefore to build the code, you will need to get the following dependencies:

  * [Maven](http://maven.apache.org)
  * [Jython](http://jython.org)
  * [Python](http://python.org)
    * [NumPy](http://numpy.scipy.org/)
    * [Matplotlib](http://matplotlib.sourceforge.net/)

In addition, if you have not used [mercurial](http://mercurial.selenic.com/downloads/) before, you will need to install its client before you can get the source code here.

### Step 1: Downloading source ###

After you have installed a [mercurial](http://mercurial.selenic.com/downloads/) client, open up a shell and run

```
hg clone https://code.google.com/p/incf-omni.examples/ incf-omni 
```

This will download the code into the incf-omni/omni-examples directory.  Inside that directory, you'll find a pom.xml file.  This is the project object model description file of the [Maven 2 build system](http://maven.apache.org).

### Step 2: Install project via maven ###

With a [Maven](http://maven.apache.org) client installed correctly and within the incf-omni/omni-core directory, run

```
mvn install
```

Maven 2 will begin installing all the java dependencies you need to run the rest, in addition to parts of the maven executable.  This will download quite a bit of required stuff, and will do some zipping and unzipping of dependencies (in a step that says "Building jar:"), so will take a little while.  Make sure that you have a version of java with the java compiler (test by typing javac on the command line).

After this is completed, go into the omni-examples directory and run the same command.

## Running examples ##

### Step 3: Set java classpath ###

Before you can run the Jython scripts, you will need to set the java classpath to point to the jar file that contains all the java dependencies.  This will be found inside the omni-examples/target directory, and should be called omni-examples-X.X.X-with-dep.jar.  In windows, you can set this with the following line in the command prompt, for example:

```
set CLASSPATH=target\omni-examples-0.0.1-SNAPSHOT-with-dep.jar
```

In unix you can set this using the following line:

```
export CLASSPATH=`pwd`/target/omni-examples-0.0.1-SNAPSHOT-with-dep.jar
```

### Step 4: Run Jython script ###

After you have installed [Jython](http://jython.org) (no version earlier than 2.5.2 will work), go into the omni-examples directory and execute:

```
jython src/main/jython/tangible_feature_export.py
```

If you have set the classpath appropriately as above, jython will start off by processing the jar you pointed it to.  If this doesn't happen, check what you set the classpath to and make sure it exists.

If this works correctly, the Jython script will access Whole Brain Catalog libraries, proceed to download some NeuroML files from the WBC server, and then will use the JUNG library to parse those NeuroML files into a file called points.txt, which will be created and put in the current directory.  The next step will need this file to be there.

### Step 5: Run Python scripts to generate results ###

After you have installed [Python](http://python.org) with the [NumPy](http://numpy.scipy.org/) module and the  [Matplotlib](http://matplotlib.sourceforge.net/) module, execute:

```
python src/main/python/distance_analysis.py
```

This will take the points from points.txt, run a distance analysis on them, and export results.txt as output.

### Step 6: Run Python scripts to export and graph results ###

To write the results out from results.txt into CSV / Excel readable format, execute:

```
python src/main/python/write_csv.py
```

To plot the results into a graph, execute:

```
python src/main/python/plot.py
```