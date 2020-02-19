<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

    <xsl:template match="//act">
        <h2>
            <a id="Act {@num}">
                <xsl:value-of select="./acttitle"/>
            </a>
        </h2>
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

    <xsl:template match="//scene">
        <h3>
            <xsl:value-of select="./scenetitle"/>
        </h3>
        <p class="stagedir">
            <xsl:value-of select="./stagedir/dir"/>
        </p>
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

    <xsl:template match="//speech">
        <div class="speech">
            <div class="speaker">
                <span>
                    <xsl:value-of select="./speaker"/>
                </span>
                <p class="line" style="position: relative;">
                    <xsl:value-of select="./line"/>
                </p>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="@* | node()">
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

</xsl:stylesheet>