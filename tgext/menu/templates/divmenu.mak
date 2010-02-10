<%
    from cgi import escape
    from tg import url
%>
<div id="${name}_div">
    <ul id="${name}" class="jd_menu${'_vertical' if vertical_menu else ''}">
<%
    def writeList(level, mlist, first=False, last=False):
        tabs = '    '*(level+2)
        if first and last:
            htmlclass = ' class="first last"'
        elif first:
            htmlclass = ' class="first"'
        elif last:
            htmlclass = ' class="last"'
        else:
            htmlclass = ""
        if mlist.href:
            href = '<a href="%s">%s</a>' % (url(mlist.href), escape(mlist.name, True))
        else:
            href = escape(mlist.name, True)
        if len(mlist.children) == 0:
            context.write('%s<li%s>%s</li>\n' % (tabs, htmlclass, href))
        else:
            context.write('%s<li%s>%s\n%s  <ul class="%s_level%s">\n' % (tabs, htmlclass, href, tabs, name, level+1))
            for child in mlist.children:
                writeList(level+1, child, child==mlist.children[0], child==mlist.children[-1])
            context.write('%s  </ul>\n' % (tabs))
            context.write('%s  </li>\n' % (tabs))
            

    for child in menulist.children:
        writeList(0, child, child==menulist.children[0], child==menulist.children[-1])
%>
    </ul>
</div>
<script type="text/javascript">
$(function(){
$("#${name}").jdMenu();
});
</script>