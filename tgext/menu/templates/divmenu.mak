<%
    from cgi import escape
    from tg import url
%>
<div id="${name}_div">
    <ul id="${name}" class="jd_menu${'_vertical' if vertical_menu else ''}">
<%
    def writeList(level, mlist):
        tabs = '    '*(level+2)
        if mlist.href:
            href = '<a href="%s">%s</a>' % (url(mlist.href), escape(mlist.name, True))
        else:
            href = escape(mlist.name, True)
        if len(mlist.children) == 0:
            context.write('%s<li>%s</li>\n' % (tabs, href))
        else:
            context.write('%s<li>%s\n%s  <ul class="%s_level%s">\n' % (tabs, href, tabs, name, level+1))
            for child in mlist.children:
                writeList(level+1, child)
            context.write('%s  </ul>\n' % (tabs))
            context.write('%s  </li>\n' % (tabs))
            

    for child in menulist.children:
        writeList(0, child)
%>
    </ul>
</div>
<script type="text/javascript">
$(function(){
$("#${name}").jdMenu();
});
</script>