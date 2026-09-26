<?xml version="1.0"?>
<!DOCTYPE stylesheet [
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
  <!ENTITY dct "http://purl.org/dc/terms/" >
  <!ENTITY sm "http://www.omg.org/techprocess/ab/SpecificationMetadata/" >
  <!ENTITY lcc-cr "https://www.omg.org/spec/LCC/Countries/CountryRepresentation/" >
  <!ENTITY lcc-3166-1 "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/" >
  <!ENTITY lcc-3166-1-adj "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes-Adjunct/" >
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
xmlns:lcc-3166-1-adj="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes-Adjunct/"
exclude-result-prefixes="xsl xs">

<!-- Takes the standard LCC Country code file and generates one additional ontology with all the countries referenced by their 2 letter code -->
<!-- with sameAs relationships to the name-based URIs in the official ontology -->

  <xsl:output method="xml" indent="yes" media-type="application/xml" use-character-maps="ampersand"/> 
  <xsl:strip-space elements="*"/>
  <!-- This is needed to allow use of XML entities such as &lcc-cr; in the output -->
  <xsl:character-map name="ampersand">
    <xsl:output-character character="&amp;" string="&#x26;"/>
  </xsl:character-map> 

  <xsl:variable name="countries-base-uri" select="'&amp;lcc-3166-1-adj;'"/>


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
    <!ENTITY lcc-3166-1 "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/" >
    <!ENTITY lcc-3166-1-adj "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes-Adjunct/" >
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
    xmlns:lcc-3166-1="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/"
    xmlns:lcc-3166-1-adj="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes-Adjunct/"
    xml:base="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes-Adjunct/">
    
  <xsl:value-of select="'&#x0A;&#x0A;'"/>
  <owl:Ontology>
      <!-- Boiler plate -->
      <xsl:attribute name="rdf:about" select="$countries-base-uri"/>
      <rdfs:label>ISO 3166-1 Country Codes Adjunct Ontology</rdfs:label>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <xsl:comment>Curation and Rights Metadata for the LCC ISO 3166-1 Country Codes Additional Ontology </xsl:comment>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <sm:copyright rdf:datatype="&amp;xsd;string">Copyright (c) 2019 Object Management Group, Inc.
        Copyright (c) 2018-2019 Adaptive Inc.
      </sm:copyright>
      <dct:license rdf:datatype="&amp;xsd;anyURI">&sm;MITLicense</dct:license>       
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <xsl:comment>Ontology/File-Level Metadata for the LCC ISO 3166-1 Country Codes Adjunct Ontology </xsl:comment>
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
    <sm:filename rdf:datatype="&amp;xsd;string">ISO3166-1-CountryCodes-Adjunct.rdf</sm:filename>
      <sm:fileAbbreviation rdf:datatype="&amp;xsd;string">lcc-3166-1-adj</sm:fileAbbreviation>
      <owl:versionIRI>
        <xsl:attribute name="rdf:resource" select="'https://www.omg.org/spec/LCC/20190201/Countries/ISO3166-1-CountryCodes-Adjunct/'"/>
      </owl:versionIRI> 
      <sm:fileAbstract rdf:datatype="&amp;xsd;string">This ontology represents an additional set of URIs for ISO 3166-1 countries, based on their 2-char codes.</sm:fileAbstract>
      <skos:changeNote>This ontology was added by the LCC 1.1 RTF</skos:changeNote>
      <dct:issued>
        <xsl:value-of select="/rdf:RDF/owl:Ontology/dct:issued"/>
      </dct:issued>        
      <xsl:value-of select="'&#x0A;&#x0A;'"/>
      <owl:imports rdf:resource="https://www.omg.org/spec/LCC/Countries/CountryRepresentation/"/>
      <owl:imports rdf:resource="https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/"/>
    <xsl:value-of select="'&#x0A;&#x0A;'"/>       
    </owl:Ontology>
    
    <xsl:call-template name="comment-block">
      <xsl:with-param name="the-text" select="'Individuals'"/>
    </xsl:call-template>
  
    <!-- Main processing -->
  <xsl:apply-templates select="rdf:RDF/owl:NamedIndividual[rdf:type/@rdf:resource='&lcc-cr;Alpha2Code']"/>
  </rdf:RDF>
</xsl:template>

<xsl:template match="owl:NamedIndividual">
   <!-- Output -->
  <lcc-cr:Country>
    <xsl:attribute name="rdf:about" select="concat($countries-base-uri, lcc-lr:hasTag)"/>
    <owl:sameAs>
      <xsl:attribute name="rdf:resource" select="lcc-lr:identifies/@rdf:resource"/>
    </owl:sameAs>
  </lcc-cr:Country>
</xsl:template>

<xsl:template match="*" priority="-1"/>

</xsl:stylesheet>
