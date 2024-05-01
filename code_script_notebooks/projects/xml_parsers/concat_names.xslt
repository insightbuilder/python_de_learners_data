<!-- concat-names.xslt -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:param name="targetDepartment" select="'IT'"/>
    
    <xsl:template match="/">
        <html>
            <body>
                <h2>Concatenated Names in Department: <xsl:value-of select="$targetDepartment"/></h2>
                <xsl:variable name="departmentWorkers" select="workers/worker[department = $targetDepartment]"/>
                <p>Names: <xsl:for-each select="$departmentWorkers"><xsl:value-of select="name"/> </xsl:for-each></p>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

