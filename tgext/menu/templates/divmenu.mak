<%
    from cgi import escape
    from tg import url
%>
<div id="${name}_div">
    <ul id="${name}" class="jd_menu${'_vertical' if vertical_menu else ''}">
<%
    def writeList(level, mlist, first=False, last=False):
        tabs = '    '*(level+2)
        if first: mlist.extras['class'].append('first')
        if last: mlist.extras['class'].append('last')
        if len(mlist.extras['class']) > 0:
            htmlclass = ' class="%s"' % (" ".join(mlist.extras['class']))
        else:
            htmlclass = ""
        attrstring = " ".join(['%s="%s"' % (x, mlist.extras[x]) for x in filter(lambda x: x not in ['class', 'extratext'], mlist.extras.keys())])
        if 'extratext' in mlist.extras:
            extratext = escape(" "+mlist.extras['extratext'])
        else:
            extratext = ""
        if attrstring: attrstring=" " + attrstring
        if mlist.href:
            href = '<a href="%s">%s</a>' % (url(mlist.href), escape(mlist.name, True))
        else:
            href = escape(mlist.name, True)
        if mlist.icon:
            imgtext = '<img src="%s" />' % (mlist.icon)
        else:
            imgtext = ''
        if len(mlist.children) == 0:
            context.write('%s<li%s%s>%s%s%s</li>\n' % (tabs, htmlclass, attrstring, imgtext, href, extratext))
        else:
            context.write('%s<li%s>%s%s\n%s  <ul class="%s_level%s">\n' % (tabs, htmlclass, href, extratext, tabs, name, level+1))
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
  $(document).ready(function() {
      $("#${name}").jdMenu();
  });
</script>
