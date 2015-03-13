

# Why is This Interesting? #

What this demonstrates is that this library is capable of accomplishing the following things:

  1. Combining XML schemas from different projects
  1. Compiling those schemas in to java objects
  1. Combining the java objects with a networking library and with a graph library
  1. Making the java objects available via Jython to a Python scripting environment

As additional XML schemas from around Neuroinformatics are added, their basic types can be made accessible as well, which means that scripts can be written that take information out of one data type and put them into another.

# An Example Usage #

This example uses a Jython/Python script to download sets of gene expression data from the Allen Brain Institute's Allen Brain Atlas (ABA) via an INCF web service, converts the XML sparse volume to Whole Brain Catalog (WBC) Java objects then to Python objects which are written to Python "pickle" files.

A second Python script reads the pickle files to Python objects. It then accesses measures of available research information about the gene from the Neuroinformatics Framework (NIF). Using the 3D points at which the gene expression level is above a threshold, the measure of available research information about the gene is used to plot a 3D "information density" scatter. Thus the plot shows in 3D brain coordinates a magnitude of available research information based on the set of genes selected for analysis.

The original input to this example are (1) the list of genes to be analyzed, and (2) the relative expression level threshold. The latter is used to limit the information density plot and facilitate meaningful visualization.

# Getting Started #

## Installing Required Libraries ##

### Step 1: Install Required Libraries ###

In order to be most general, OMNI takes advantage of libraries in both Python and Java.  Therefore to run this example, you will need to install the following libraries:

  * [Java Runtime (JRE)](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
  * [Jython](http://jython.org)
  * [Python](http://python.org)
    * [NumPy](http://numpy.scipy.org/)
    * [Matplotlib](http://matplotlib.sourceforge.net/)

## Building from Source ##

**NOTE**: If you want to skip building from source (steps 2, 3, and 4), you can
  * download a pre-built zip from the [downloads section](http://code.google.com/p/incf-omni/downloads/list) (named like omni-examples-1.0.0-all.zip)
  * unzip the file which will have a directory name like omni-examples-1.0.0
  * skip to [step 5](GettingStartedInformationDensityPlot#Running_this_Example.md).

### Step 2: Install Required Build Packages ###

You will need to install the following packages:

  * [Maven](http://maven.apache.org)
  * [Mercurial](http://mercurial.selenic.com/downloads/)

### Step 3: Download Source ###

After you have installed a [mercurial](http://mercurial.selenic.com/downloads/) client, open up a shell and run

```
$ hg clone https://code.google.com/p/incf-omni.examples/ incf-omni.examples 
```

This will download the code into the incf-omni.examples directory.  Inside that directory, you'll find a pom.xml file.  This is the project object model description file of the [Maven 2 build system](http://maven.apache.org).

### Step 4: Install Project via Maven ###

With a [Maven](http://maven.apache.org) client installed correctly and within the incf-omni/omni-core directory, run

```
$ mvn install
```

Maven 2 will begin installing all the java dependencies you need to run the rest, in addition to parts of the maven executable.  This will download quite a bit of required stuff, and will do some zipping and unzipping of dependencies (in a step that says "Building jar:"), so will take a little while.  Make sure that you have a version of java with the java compiler (test by typing javac on the command line).

After this is completed, go into the incf-omni.examples directory and run the same command.

## Running this Example ##

### Step 5: Change to the Correct Directory ###

This will be the directory in which you unzipped the pre-built zip file or built the examples from source.

### Step 6: Set Java Classpath ###

Before you can run the Jython scripts, you will need to set the java classpath to point to the jar file that contains all the java dependencies.  This will be found inside the omni-examples/target directory, and should be called omni-examples-X.X.X-with-dep.jar.  In windows, you can set this with the following line in the command prompt, for example:

```
>set CLASSPATH=target\omni-examples-1.0.0-with-dep.jar
```

In unix you can set this using the following line:

```
$ export CLASSPATH=`pwd`/target/omni-examples-1.0.0-with-dep.jar
```

### Step 7: Edit Config Files ###

As mentioned above there are two config files which can be edited to control input values to this example:

  * genelist.txt
  * trimpercent.txt

You can use any text editor such as vi, gedit, emacs, Notepad, etc.

Both are fully documented with comment lines. Comment lines begin with the pound symbol (#). Other uncommented lines are actual input values to the example.

In genelist.txt the uncommented lines determine what genes will be analyzed. On separate lines put the ABA gene symbol and the entrez gene id, separated by a comma and a space, of the genes you wish to analyze.

Similarly in trimpercent.txt there is one uncommented line which determines the percent of non-zero expression values to be retained. The commented lines in this file explain the action. Put the desired value on a single uncommented line.

### Step 8: Run Jython Script ###

After you have installed [Jython](http://jython.org) (no version earlier than 2.5.2 will work), go into the incf-omni.examples directory and execute:

```
$ jython src/main/jython/gene_expression_import.py
```

If you have set the classpath appropriately as above, jython will start off by processing the jar you pointed it to.  If this doesn't happen, check what you set the classpath to and make sure it exists.

If this works correctly, the Jython script will
  * Access gene expression data from the Allen Brain Atlas via the INCF Atlas Hub server
  * Download gene expression sparse volume data for the genes to be analyzed (specified in the genelist.txt config file)
  * Convert the data into Python objects (specified by the SparseVolumeData class defined in volume\_data.py)
  * Write the objects to Python "pickle" file(s) for use in subsequent steps

The next step will need the pickle file(s) to be there. The pickle files will be named "sparseVolume[entrez-gene-id].pkl". E.g., "sparseVolume12810.pkl".

### Step 9: Run Python Scripts to Generate Results ###

After you have installed [Python](http://python.org) with the [NumPy](http://numpy.scipy.org/) and [Matplotlib](http://matplotlib.sourceforge.net/) modules, execute:

```
$ python src/main/python/info_density_plot.py
```

This will

  * Read the expression data from the sparseVolumeNNNNN.pkl file(s) back into Python objects
  * Reduce the 3D point density based on the config file trimpercent.txt (described above)
  * Access  measures of available research information about the gene(s) from the Neuroinformatics Framework (NIF)
  * At the 3D points that indicate gene expression, replace the values with information measures
  * Aggregate the information measures across the genes at each 3D point
  * Plot a 3D scatter diagram that will at each point show the aggregated information measures

# Summary of Scripts and Files in this Example #

All scripts and files are under the parent directory: incf-omni.examples. The purpose of these files is described above. Note there are other scripts and files that are not listed here because they relate to other example applications.

## Config Files ##

  * genelist.txt
  * trimpercent.txt

## Python Library Script ##

  * src/main/python/volume\_data.py

## Executable Python/Jython Scripts ##

  * src/main/jython/gene\_expression\_import.py
  * src/main/python/info\_density\_plot.py

## Data Transfer Files ##

  * sparseVolumeNNNNN.pkl - Intermediate data transfer files. These are Python "pickle" files that contain sparse volume gene expression data in Python objects.