<%
    from cgi import escape
%>
<div id="${name}_div">
    <ul id="${name}">
<%
    prev = []
    prevfullpath = []
    tab = '    '
    for i, entry in enumerate(menulist):
        fullpath = [x.strip() for x in entry[0].split('||')]
        current = fullpath[:-1]
        if i != 0 and current[:len(prevfullpath)] != prevfullpath:
            context.write('</li>\n')
        if current == prev:
            context.write('<li><a href="%s">%s</a>' % (entry[1], escape(fullpath[-1], True)))
        else:
            if len(current) == len(prev):
                context.write('</ul>\n')
                context.write('</li>\n')
                context.write('<li><a href="%s">%s</a>' % (entry[1], escape(fullpath[-1], True)))
            elif len(current) > len(prev):
                for idx in range(len(prev), len(current)):
                    context.write('\n<ul>\n')
                    context.write('<li>%s' % (current[idx]))
                context.write('\n<ul>\n')
                context.write('<li><a href="%s">%s</a>' % (entry[1], escape(fullpath[-1], True)))
            else:
                context.write('</li>\n')
                for idx in range(len(current), len(prev)):
                    context.write('</ul>\n')
                    context.write('</li>\n')
        prevfullpath = fullpath
        prev = current
    if len(menulist) > 0:
        context.write('</li>\n')
%>
    </ul>
</div>
