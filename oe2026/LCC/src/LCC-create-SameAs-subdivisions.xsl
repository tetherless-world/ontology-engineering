<?xml version="1.0"?>
<!DOCTYPE stylesheet [
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
  <!ENTITY dct "http://purl.org/dc/terms/" >
  <!ENTITY sm "http://www.omg.org/techprocess/ab/SpecificationMetadata/" >
  <!ENTITY lcc-cr "https://www.omg.org/spec/LCC/Countries/CountryRepresentation/" >
  <!ENTITY lcc-3166-2 "https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes/" >
  <!ENTITY lcc-3166-2-adj "https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes-Adjunct/" >
]>

<!-- This file is copyright 2018-2019, Adaptive Inc.  -->
<!-- All rights reserved. -->
<!-- A limited license is provided to use and modify this file purely for the purpose of maintaining the ontology 
     in the OMG specification "Languages Countries and Codes (LCC)" and purely by members of the LCC Revision Task Force (RTF)  -->
<!-- IT MAY NOT, IN WHOLE OR PART, BE USED, COPIED, DISTRIBUTED, MODIFIED OR USED AS THE BASIS OF ANY DERIVED WORK OR 
     FOR ANY OTHER PURPOSE -->
<!-- To license for any other purpose, please contact info@adaptive.com -->


<xsl:stylesheet version="2.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xmlns:owl="http://www.w3.org/2002/07/owl#"
xmlns:skos="http://www.w3.org/2004/02/skos/core#" 
xmlns:dct="http://purl.org/dc/terms/"
xmlns:xsd ="http://www.w3.org/2001/XMLSchema#"
xmlns:sm="http://www.omg.org/techprocess/ab/SpecificationMetadata/" 
xmlns:lcc-lr="https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/"
xmlns:lcc-cr="https://www.omg.org/spec/LCC/Countries/CountryRepresentation/"
xmlns:lcc-3166-2-adj="https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes-Adjunct/"
xmlns:lcc-639-1="https://www.omg.org/spec/LCC/Languages/ISO639-1-LanguageCodes/"
xmlns:lcc-639-2="https://www.omg.org/spec/LCC/Languages/ISO639-2-LanguageCodes/"
xmlns:lcc-3166-1="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/"

xmlns:file="http://expath.org/ns/file"
extension-element-prefixes="file"
exclude-result-prefixes="xsl xs lcc-639-1 lcc-639-2 lcc-3166-1">

<!-- Takes the standard LCC Regions files and generates one additional ontology with all the countries referenced by their 4-5 letter subdivision code -->
<!-- with sameAs relationships to the name-based URIs in the official ontology -->
<!-- Note: input file should be the generated ISO3166-1-CountryCodes.rdf file since that has the correct dct:issued ate -->

  <xsl:output method="xml" indent="yes" media-type="application/xml" use-character-maps="ampersand"/> 
  <xsl:strip-space elements="*"/>
  <!-- This is needed to allow use of XML entities such as &lcc-cr; in the output -->
  <xsl:character-map name="ampersand">
    <xsl:output-character character="&amp;" string="&#x26;"/>
  </xsl:character-map> 

  <xsl:variable name="subdivs-base-uri" select="'&amp;lcc-3166-2-adj;'"/>


<!-- Displays supplied text in a highly visible comment block -->
<!-- Currently uses style from OWL API -->
<xsl:template name="comment-block">
  <xsl:param name="the-text"></xsl:param> <!-- What to display in the block -->
  <xsl:text>

  </xsl:text>
  <xsl:comment>
    <xsl:text>
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // </xsl:text><xsl:value-of select="$the-text"/><xsl:text>
    //
    ///////////////////////////////////////////////////////////////////////////////////////
    </xsl:text>
  </xsl:comment>
  <xsl:text>
</xsl:text>
</xsl:template>


<xsl:template match="/">
  <xsl:text disable-output-escaping="yes"> 
<![CDATA[<!DOCTYPE rdf:RDF [
    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
    <!ENTITY dct "http://purl.org/dc/terms/" >
    <!ENTITY sm "http://www.omg.org/techprocess/ab/SpecificationMetadata/" >
    <!ENTITY lcc-cr "https://www.omg.org/spec/LCC/Countries/CountryRepresentation/" >
    <!ENTITY lcc-3166-2-adj "https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes-Adjunct/" >
    ]> ]]>
</xsl:text>    
  
<rdf:RDF      
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:dct="http://purl.org/dc/terms/"
    xmlns:sm="http://www.omg.org/techprocess/ab/SpecificationMetadata/"
    xmlns:lcc-cr="https://www.omg.org/spec/LCC/Countries/CountryRepresentation/"
    xmlns:lcc-lr="https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/"
    xmlns:lcc-3166-2-adj="https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes-Adjunct/"
    xml:base="https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes-Adjunct/">
    
  <xsl:variable name="dir" select="file:parent(document-uri(/))"/>
  
  <xsl:value-of select="'&#x0A;&#x0A;'"/>
  <owl:Ontology>
      <!-- Boiler plate -->
      <xsl:attribute name="rdf:about" select="$subdivs-base-uri"/>
      <rdfs:label>ISO 3166-2 Subdivision Codes Adjunct Ontology</rdfs:label>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <xsl:comment>Curation and Rights Metadata for the LCC ISO 3166-2 Subdivision Codes Adjunct Ontology </xsl:comment>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <!--Curation and Rights Metadata for the LCC ISO 3166-1 Country Codes Additional Ontology -->
      
      <sm:copyright rdf:datatype="&xsd;string">Copyright (c) 2015-2021 Object Management Group, Inc.</sm:copyright>
      <sm:copyright rdf:datatype="&xsd;string">Copyright (c) 2015-2020 Adaptive Inc.</sm:copyright>
      <sm:copyright rdf:datatype="&xsd;string">Copyright (c) 2021 agnos.ai UK Ltd.</sm:copyright>
      <sm:copyright rdf:datatype="&xsd;string">Copyright (c) 2015-2021 Thematix Partners LLC</sm:copyright>
      <sm:copyright rdf:datatype="&xsd;string">Copyright (c) 2015-2017 Unisys</sm:copyright>
      <dct:license rdf:datatype="&xsd;anyURI">http://opensource.org/licenses/MIT</dct:license>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <xsl:comment>Ontology/File-Level Metadata for the LCC ISO 3166-2 Subdivision Codes Adjunct Ontology </xsl:comment>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <sm:filename rdf:datatype="&amp;xsd;string">ISO3166-2-SubdivisionCodes-Adjunct.rdf</sm:filename>
      <sm:fileAbbreviation rdf:datatype="&amp;xsd;string">lcc-3166-2-adj</sm:fileAbbreviation>
      <owl:versionIRI>
        <xsl:attribute name="rdf:resource" select="'https://www.omg.org/spec/LCC/20211101/Countries/ISO3166-2-SubdivisionCodes-Adjunct/'"/>
      </owl:versionIRI> 
      <sm:fileAbstract rdf:datatype="&amp;xsd;string">This ontology represents an additional set of URIs for ISO 3166-2 subdivisions, based on their 2-char+2/3 char codes.</sm:fileAbstract>
      <skos:changeNote>This ontology was added by the LCC 1.1 RTF</skos:changeNote>
      <skos:changeNote>This ontology was amended by the LCC 1.2 RTF to reflect the updated URIs</skos:changeNote>
      <dct:issued>
        <xsl:value-of select="/rdf:RDF/owl:Ontology/dct:issued"/>
      </dct:issued>        
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <owl:imports rdf:resource="https://www.omg.org/spec/LCC/Countries/CountryRepresentation/"/>
      <owl:imports rdf:resource="https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes/"/>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>       
    </owl:Ontology>
    
    <xsl:call-template name="comment-block">
      <xsl:with-param name="the-text" select="'Individuals'"/>
    </xsl:call-template>
  
    <!-- Main processing -->
    <xsl:call-template name="process-dir">
      <xsl:with-param name="dir" select="$dir"/>
    </xsl:call-template>
  </rdf:RDF>
</xsl:template>
  
  <xsl:template name="process-dir">
    <xsl:param name="dir"/>
    <xsl:for-each select="file:children($dir)[contains(., '.rdf')]">
      <xsl:variable name="filename" select="file:path-to-uri(.)"/>
      <!-- <xsl:message select="concat('Processing file: ', $filename)"/> -->       
      <xsl:variable name="rdf" select="document($filename)/rdf:RDF"/>
      <xsl:variable name="xmlbase" select="$rdf/@xml:base"/>
      <xsl:variable name="ontology" select="$rdf//owl:Ontology[1]"/>
      <xsl:variable name="ontology-uri" select="$ontology/@rdf:about"/>
      <xsl:apply-templates select="$rdf/owl:NamedIndividual[rdf:type/@rdf:resource='&lcc-cr;GeographicRegionIdentifier']"/>
      
    </xsl:for-each>
    <!-- recurse -->
    <xsl:for-each select="file:children($dir)">
      <xsl:if test="file:is-dir(.) and not(contains(., '1.') or ends-with(., '.git') or ends-with(., 'etc'))">
        <xsl:call-template name="process-dir">
          <xsl:with-param name="dir" select="."/>
        </xsl:call-template>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>
  

<xsl:template match="owl:NamedIndividual">
  <xsl:variable name="it" select="lcc-lr:identifies/@rdf:resource"/>
  <xsl:variable as="element()" name="item" select="//owl:NamedIndividual[@rdf:about=$it][1]"/>
  <xsl:variable name="type">
    <xsl:choose>
      <xsl:when test="contains($item/rdf:type[1]/@rdf:resource, 'Territory')">lcc-cr:Territory</xsl:when>
      <xsl:when test="contains($item/rdf:type[1]/@rdf:resource, 'CountrySubdivision')">lcc-cr:CountrySubdivision</xsl:when>
      <xsl:otherwise>
        <xsl:message select="concat('Unknown region type of ', $item/rdf:type[1]/@rdf:resource, ' for ', $it)"/>
        <xsl:text>lcc-cr:CountrySubdivision</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
   <!-- Output -->
  <xsl:element name="{$type}">
    <xsl:attribute name="rdf:about" select="concat($subdivs-base-uri, lcc-lr:hasTag)"/>
    <owl:sameAs>
      <xsl:attribute name="rdf:resource" select="lcc-lr:identifies/@rdf:resource"/>
    </owl:sameAs>
  </xsl:element>
</xsl:template>

<xsl:template match="*" priority="-1"/>

</xsl:stylesheet>
