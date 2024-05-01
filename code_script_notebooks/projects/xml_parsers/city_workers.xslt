<!-- city-workers.xslt -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:key name="city-key" match="worker" use="city"/>
    
    <xsl:template match="/">
        <html>
            <body>
                <h2>Workers by City</h2>
                <xsl:for-each select="workers/worker[count(. | key('city-key', city)[1]) = 1]">
                    <h3><xsl:value-of select="city"/></h3>
                    <ul>
                        <xsl:variable name="currentCity" select="city"/>
                        <xsl:for-each select="key('city-key', $currentCity)">
                            <li><xsl:value-of select="name"/> - <xsl:value-of select="position"/></li>
                        </xsl:for-each>
                    </ul>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

