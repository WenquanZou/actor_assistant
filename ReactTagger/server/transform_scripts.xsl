<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>

    <!--Root node-->
    <xsl:template match="//act">
        <h2>
            <a id="Act {@num}">
                <xsl:value-of select="./acttitle"/>
            </a>
        </h2>
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

    <xsl:template match="scene">
        <h3>
            <a id="Act {@actnum} Scene {@num}">
                <xsl:value-of select="./scenetitle"/>
            </a>
        </h3>
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

    <xsl:template match="speech">
        <div class="speech">
            <div class="speaker">
                <span>
                    <xsl:value-of select="./speaker"/>
                </span>
                <xsl:apply-templates select="@* | node()"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="scene/stagedir">
        <p class="stagedir" id="Stagedir {@sdglobalnumber}">
            <xsl:value-of select="current()/dir"/>
        </p>
    </xsl:template>

    <!--Leaf node-->
    <xsl:template match="speech/line">
        <p class="line" id="Line {@globalnumber}" style="position: relative;">
            <xsl:value-of select="current()"/>
        </p>
    </xsl:template>

    <xsl:template match="speech/stagedir">
        <p class="stagedir" id="Stagedir {@sdglobalnumber}">
            <xsl:value-of select="current()/dir"/>
        </p>
    </xsl:template>

    <!--Default node: DO NOT copy any contents-->
    <xsl:template match="@* | node()">
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>

</xsl:stylesheet>