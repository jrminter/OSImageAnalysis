# Plug-in development in Fiji

1. Fiji Needs Java

2. Java version:  At least 1.8

3. Eclipse. Download. Match 32/64 on Win

4. Use Java version of Eclipse

5. Download the current Fiji application Download

6. Download the example plugins

    - [ImageJ2](https://github.com/imagej/example-imagej-command)
    - [ImageJ1](https://github.com/imagej/example-legacy-plugin/)


## Files needed:

- Eclipse installer (tar.gz)
- example-imagej-command
- Fiji App
- jdk8


# Steps

1. Uncompress the example

2. Edit pom.xml. It has the important configuration info

3. More [info](https://imagej.net/Maven#POM_and_directory_structure).

4. POM and directory structure

    All it really takes is a `pom.xml` file and a certain directory structure:

```
pom.xml
src/
   main/
       java/
           <package>/
                    <name>.java
                    ...
       resources/
                <other-files>
                ...
```

- Technically, you can override the default directory layout in the pom.xml, but why do so? It only breaks expectations and is more hassle than it is worth, really.

- So the directory structure is: you put your .java files under `src/main/java/` and the other files you need to be included into `src/main/resources/`. Should you want to apply the best practices called "regression tests" or even "test-driven development": your `tests.java` files go to `src/test/java/` and the non-.java files you might require unsurprisingly go into `src/test/resources/`.


## Simple `pom.xml` example:

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
    http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
 
  <groupId>org.mywebsite</groupId>
  <artifactId>my-uber-library</artifactId>
  <version>2.0.0-SNAPSHOT</version>
</project>
```

The first 6 lines are of course just a way to say "Hi, Maven? How are you today? This is what I would like you to do...".

The only relevant parts are the groupId, which by convention is something like the inverted domain name (similar to the Java package convention), the name of the artifact to build (it will be put into target/, under the name <artifactId>-<version>.jar). And of course the version.

Dependencies
Maven is not only a build tool, but also a dependency management tool.

To depend on another library, you must declare the dependencies in your project's pom.xml file. For example, every ImageJ 1.x plugin will depend on ImageJ 1.x. So let's add that (before the final </project> line):

```
<dependencies>
  <dependency>
    <groupId>net.imagej</groupId>
    <artifactId>ij</artifactId>
    <version>1.45b</version>
  </dependency>
</dependencies>
```

As you can see, dependencies are referenced using the same groupId, artifactId and version triplet (also known as GAV parameters) that you declared for your project itself.


## Change the example data

1. Edit the group id convention:  -name

2. Choose an Artifact-ID (i.e. No spaces or "-") 

3. Enter the version number

4. Enter the name (Can have spaces...)

5. Enter a short description

6. Enter a web page where people can find info about you/the plug-in

7. Enter web page and name of your organization

8. Enter developer's ID and info

9. Enter contributor's info (if you have them...)

10. When done, save and close the file








