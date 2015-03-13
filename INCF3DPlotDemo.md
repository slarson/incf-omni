# incf-omni.examples #

## Files (incf-omni.examples) ##
  * genelist.txt - list of genes to examine
  * trimpercent.txt - specifies trimming expression data
  * src/main/jython/gene\_expression\_import.py -
  * src/main/python/volume\_data.py - class definitions
  * src/main/python/info\_density\_plot.py -

## Sequence of Operations ##
  * $ jython src/main/jython/gene\_expression\_import.py
    * get list of target genes from text file
    * for each gene
      * get sparse volume data
      * extract entrez gene id and gene symbol
      * initialize sparse volume data object
      * "pickle" the object to a file
  * $ python src/main/python/info\_density\_plot.py
    * get list of target genes from text file
    * get trim percent value from text file
    * for each gene
      * "unpickle" the sparse volume data object
      * trim the object retaining only the highest 75% of gene expression values
      * get and scale NIF total hits for gene
      * replace expression values with scaled NIF hits for gene
      * find overall max x, y, and z coordinates across all genes
    * create 3D array based on max coordinates and initialized to zero
    * for each gene now with NIF hits at each expression point
      * aggregate hits at each point
    * convert 3D array to sparse volume object
    * produce 3D scatter plot