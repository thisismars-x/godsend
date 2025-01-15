
#     God, Jesus, Yeshua, Creator.
#
#     ||||||||||||||||||||||||||
#              GODSEND
#     ||||||||||||||||||||||||||
#
# godsend is a backend engine with its own
# routing primitives and its own template engine
#
# the goals for godsend are @goals
# godsend has everything you need to create
# websites and deploy servers
# and has a wsgi- compliant app interface.
# read more at godsleather


# base class for dealing with exceptions
class godinpain(Exception): pass

class routeerror(godinpain): pass
class templateerror(godinpain): pass
class viewerror(godinpain): pass
class internalerror(godinpain): pass

def nothing(): pass

import re
class Router:
    '''God hates when men ask for multiple app instances.
    Use one app, let Router become exclusively global for your runtime'''

    def __init__(self, rule: str):
        self.rule = rule

    def __call__(self, incoming_url: str):
        return self.match(incoming_url)

    def match(self, incoming_url: str):
        (compile_rule, stat) = self.x_compile()
        # resolving a later bug
        # if stat is true simply match the two strings 
        # and return True or False
        # BUG:
        # if dynamic routes fail they return {} (no context)
        # static routes always give {} (as they have no context)

        if stat:
           return incoming_url.removeprefix('/') == self.rule.removeprefix('/')

        valid = self.check_validity(compile_rule)
        if not valid: raise routeerror("Your rule seems to have types that are not :valid_types:'list'")

        return self.process(compile_rule, incoming_url)

    def x_compile(self):
        dyn = True if '<' in self.rule else False
        stat_groups = dict()

        rule = self.rule.removeprefix('/') if self.rule[0] == '/' else self.rule
        _all_list = rule.split('/')

        if not dyn:
            for groups in _all_list:
                # 'stat' is for marking a field static
                # for /home/<int:age>/peso, home and peso would be marked 'stat'
                stat_groups.update( {f'{groups}': 'stat'} )
            return (stat_groups, not dyn)

        dyn_groups = dict()
        for groups in _all_list:
            if groups != '':
                if '<' in groups:
                    groups = groups.replace('<', '').replace('>', '')
                    if ':' in groups:
                        _type, _name = groups.split(':')
                        dyn_groups.update( {f'{_name.strip()}' : f'{_type.strip()}'} )
                    else:
                        # 'str' is inferred type when typing is not explicit
                        # <person> and <str: person> are equivalent
                        dyn_groups.update( {f'{groups.strip()}': 'str' } )
                else:
                    dyn_groups.update( {f'{groups}' : 'stat'} )
        dyn_groups.update( { '': 'stat' } ) if rule[-1] == '/' else nothing()
        return (dyn_groups, not dyn)

    def check_validity(self, compiled_url: dict):
        # it is not that crazy a idea to only allow for explicit regular
        # expressions in your url. For convenience, valid_types has several
        # types that map into regular expressions. Other than these types,
        # leave for type inference('str') or else use regular expressions
        # if needed

        _valid_types = [ 'str', 'int', 'path' ]
        if set(compiled_url.values()) <= set(_valid_types + ['stat']): return True

        for types in compiled_url.values():
            if types.startswith('['):
                try:
                    types = types[1:-1]
                    cxmpile = re.compile(types)
                except re.error:
                    raise routeerror("Could not compile your regular expressions in your url-rule")
                    return False
            else:
                if types not in _valid_types + ['stat']: return False
        return True
        
    def process(self, compile_rule, incoming_url):
        '''One beautiful component of using Godsent is, all url-rules compile into a glob of regex
        no matter dynamic or static. At this point, there is no way to say if our rule was static
        or dynamic. It is not static or dynamic- it is a regex compiled expression'''
        
        _cc = str()
        for (k, v) in compile_rule.items():
            if v[0] == '[':
                 _cc += f'(?P<{k}>{v[1: -1]})' + '/'
                 continue

            match v:
                 case 'stat':
                      _cc += k + '/' if k != "" else ""
                 case 'int':
                      _cc += f'(?P<{k}>[0-9]+)' + '/'
                 case 'str':
                      _cc += f'(?P<{k}>[a-zA-Z0-9]+)' + '/'
                 case 'path':
                      _cc += f'(?P<{k}>([a-zA-Z0-9]+/)*[a-zA-Z0-9]+)' + '/'

        if self.rule[-1] != '/' and _cc[-1] == '/': _cc = _cc[:-1]
        if self.rule[-1] == '/' and _cc[-1] != '/': _cc += '/'

        try: _recompile_url = re.compile(_cc)
        except: raise routeerror("Your regular expressions are invalid")

        incoming_url = incoming_url if incoming_url[0] != '/' else incoming_url[1:]
        matches = re.match(_recompile_url, incoming_url)
        return matches.groupdict() if matches is not None else dict()

# example
# rule = 'home/login/<str:user>/<int:id>/digital/nomad/lives/<condition>/<[[0-4]{4}]:s>'
# match = 'home/login/avi/1000/digital/nomad/lives/terrible/1010'
# route = Router(rule)
# print(route(match))

# God says, to ditch a template engine we should write a new template engine
# Well, python is turing-complete. Why introduce other turing complete
# languages, when by definition, a turing complete language should be
# capable of simulating another turing complete language completely.
# Reject Jinja, Jinja2, DTL, use python in your templates

# to ditch a template engine first python needs to work within templates
import re
class templerser:
    
    # the backend for your template engine
    _tokens_all = r'''(
        [uUrRbB]*
        (?:     ''(?!') 
                |""(?!")
                |'{6}
                |"{6}
                |'(?:[^\\']|\\.)+?' 
                |"(?:[^\\"]|\\.)+?"
                |'{3}(?:[^\\']|\\.|\n)+?'{3}
                |"{3}(?:[^\\"]|\\.|\n)+?"{3}
        )
    )'''

    # inline tokens
    _cd_incl = _tokens_all.replace(r'|\n', '') 

    # comments and brackets
    _tokens_all = '(?mx)' + _tokens_all + r'''|(\#.*)|([\(\[\{])|([\)\]\}]) ''' 

    # a new python block or line is started with % or <% alone
    _cd_split = r'''(?m)^[ \t]*(\\?)((%)|(<%))'''

    # a inclusive block begins with {{ and ends with }}
    _cd_incl = r'''{{((?:%s|[^'"\n])*?)}}''' % _cd_incl
    _cd_incl = '(?mx)' + _cd_incl

    _tokens_all += r'''       
        # the labelled parts of python 
        |^([\ \t]*(?:if|for|while|try|class|def|with)\b)
        |^([\ \t]*(?:elif|else|except|finally)\b)
    
        # end alone ends a % block
        |((?:^|;)[\ \t]*end[\ \t]*(?=(?:%>[\ \t]*)?\r?$|;|\#))
        |(%>[\ \t]*(?=\r?$))
        |(\r?\n)
    '''
    _re_cache = list()
    _re_cache.extend([re.compile(x) for x in (_cd_split, _tokens_all, _cd_incl)])

    def __init__(self, src: str):
        self.src = src

        # order: block start, block end, line start, inline block start, inline block end
        self._tokens = ['<%', '%>', '%', '{{', '}}']
        self.line_no, self.offset = 1, 0
        self.indent, self.indent_mod = 0, 0
        self.parent_depth = 0

        self.text_buf, self.code_buf = list(), list()

    def _cd_translate(self):
        if self.offset: raise templateerror("Error translating")

        while True:
            m = self._re_cache[0].search(self.src, pos=self.offset) 
            
            if m:
                text = self.src[self.offset:m.start()]
                self.text_buf.append(text)
                self.offset = m.end()

                if m.group(1):
                    line, _, _ = self.src[self.offset:].partition('\n')
                    self.offset += len(line + '\n')
                    self.text_buf.append(self.src[m.start():m.start(1)] + m.group(2) + line + '\n')
                    continue
                
                self.flush_text()
                self.offset += self.read_code(self.src[self.offset:], multiline=bool(m.group(4)))
            else:
                break

        self.text_buf.append(self.src[self.offset:])
        self.flush_text()
        return ''.join(self.code_buf)
        
    def flush_text(self):
        text = ''.join(self.text_buf)
        del self.text_buf[:]
        if not text: return

        # new lines will look like \\\n 
        parts, pos, nl = list(), 0, '\\\n' + '  ' * self.indent

        for m in self._re_cache[2].finditer(text):
            prefix, pos = text[pos:m.start()], m.end()
            if prefix: parts.append(nl.join(map(repr, prefix.splitlines(True))))
            if prefix.endswith('\n'): parts[-1] += nl

            parts.append(self.process_inline(m.group(1).strip()))

        if pos < len(text):
            prefix = text[pos:]
            lines = prefix.splitlines(True)

            if lines[-1].endswith('\\\\n'): lines[-1] = lines[-1][:-3]
            elif lines[-1].endswith('\\\\\r\n'): lines[-1] = lines[-1][:-4]
            parts.append(nl.join(map(repr, lines)))
        
        code = '_printlist((%s,))' % ', '.join(parts)
        self.line_no += code.count('\n') + 1
        self.write_code(code)

    def read_code(self, pysrc, multiline):
        code_line, cmmt = '', ''
        offset = 0

        while True:
            m = self._re_cache[1].search(pysrc, pos=offset)

            if not m:
                code_line += pysrc[offset:]
                offset = len(pysrc)
                self.write_code(code_line.strip(), cmmt)
                break

            code_line += pysrc[offset:m.start()]
            offset = m.end()

            _str, _com, _po, _pc, _blk1, _blk2, _end, _cend, _nl = m.groups()

            if self.parent_depth > 0 and (_blk1 or _blk2):
                code_line += _blk1 or _blk2
                continue
            
            if _str: code_line += _str
            elif _com:
                cmmt = _com
                if multiline and _com.strip().endswith(self._tokens[1]):
                    multiline = False

            elif _po: # paranthesis open
                self.parent_depth += 1
                code_line += _po

            elif _pc: # paranthesis closed
                if self.parent_depth > 0:
                    self.parent_depth -= 1
                code_line += _pc

            elif _blk1:
                code_line = _blk1 # if/for/while/..
                self.indent += 1
                self.indent_mod -= 1

            elif _blk2: # else/elif/except..
                code_line = _blk2
                self.indent_mod -= 1

            elif _cend: # '%>'
                if multiline: multiline = False
                else: code_line += _cend

            elif _end:
                self.indent -= 1
                self.indent_mod += 1

            else:
                # \n
                self.write_code(code_line.strip(), cmmt)
                self.line_no += 1

                code_line, cmmt, self.indent_mod = '', '', 0
                if not multiline: break

        return offset
    
    @staticmethod
    def process_inline(chunk):
        if chunk[0] == '!': return '_str(%s)' %chunk[1:]
        return '_escape(%s)' %chunk

    def write_code(self, line, cmmt=''):
        code = '  ' * (self.indent + self.indent_mod)
        code += line.lstrip() + cmmt + '\n'

        self.code_buf.append(code)

from functools import partial, cached_property
class temple:
    # the frontend for your template engine
    # can be invoked as easily as fn: temples, but it is better
    # for you to use fn: temples.
    
    settings, defaults = dict(), dict()
    _std_env = dict()
    
    def __init__(self, source=None, **settings):
        self.source = ""
        _is_file = False

        try:
            with open(source, 'r') as f:
                self.source = f.read()
                _is_file = True
        except:
            self.source = source

        self.fname = source if _is_file else None
        self.seetings = self.settings.copy()
        self.settings.update(settings)
        self._std_env.update({ '_str': _str, '_escape': _escp_html, })
        
        self.prepare(**self.settings)

    def prepare(self, noescape=False, **kwargs):
        self.cache = {}

    def _exec(self, _stdout, kwargs):
        
        env = self.defaults.copy()

        env.update(kwargs)
        env.update(self._std_env)
        
        # extra functionality from within the templates
        # see more at the end
        env.update({
            '_stdout': _stdout,
            '_printlist': _stdout.extend,
            'get': env.get,
            'setdefault': env.setdefault,
            'defined': env.__contains__
        })

        exec(self.co, env)
        return env

    def render(self, *args, **kwargs):
        env, stdout = dict(), list()

        for arg in args:
            env.update(arg)

        env.update(kwargs)
        self._exec(stdout, env)
        return ''.join(stdout)

    @cached_property
    def code(self):
        source = self.source
        if not source:
            with open(self.fname, 'rb') as f:
                source = f.read()
        source = _str(source)
        parser = templerser(source)
        return parser._cd_translate()

    @cached_property
    def co(self):
        return compile(self.code, self.fname or '<string>', 'exec')
    
def _escp_html(text):
    return text.replace('&', '&amp;')\
            .replace('>', '&gt;').replace('<', '&lt;')\
            .replace('"', '&quot;').replace("'", '&#039;')
    
def _str(text: str):
    return "" if text is None else str(text)

# Files are looked for in :directory -> lookup_at 
# with :extensions -> supported_extension
supported_extensions = ['html'] + ['godsleather', 'godsword', 'godsworld']
lookup_at = [''] + ['temples/']

# Almost exclusively use fn-temples when using templates instead of class-temple
# Some helpful grammar in my templates:
# valid python code is fine. Meaning your template can have classes, functions and
# anything else python has.
# For convenience, a handful of functions have been made accessible.
# you can use get(variable_name) to get value of that variable in that active context
# you can use defined(variable_name) to check if the template defines it in that active context
# you can use setdefault(variable_name, value) to set some variable = value
import pathlib
def temples(src, **kwargs) -> str:
    # get a rendered template
    # src should be filename or template string
    # **kwargs is the active context for this template
    # class: temple is the frontend for designing templates
    # fn: temples is an extension of this, it just makes things
    # a little more convenient.
    # rendered template <-- [ temples ---> ] temple --> templerser
    # [*] is just a convenience
    
    fname = False
    _lookup_at = kwargs.pop('template_lookup', lookup_at)
    
    _src = ''
    for i in lookup_at:
        _src = i + src
        if pathlib.Path(_src).is_file():
            fname = True

            if src.split('.')[-1] not in supported_extensions:
                raise templateerror('Wrong file extension')
                
            break

    if not fname: _src = src
    _internal_temple = temple(_src)
    return _internal_temple.render(kwargs)

# examples
#
# additional context is always immutably escaped.
# do not do things that do not need to be done
# more code is not always bad. DRY is killing the culture
# more = { 'g'  : 'ods',  'oods' : 'aregood' }
# yeshua = temples(r'''
# <html>
#    <body>
#    .... we still the kids we used to be(eee)
#    .... and nothing hurts anymore
#    .... i feel
#    ....
#    % for i in range(10):
#       <p> i feel kinda free </p>
#    % end
#    This must be {{ creator }}'s plan.
#    I have been up for 25 hours.
#    {{ creator }}

#    <%
#      import os
#      __os__name = os.name
#      name = "Terry Davis"
#    %>
#    <p> God is mostly engaged in {{ os.name }} </p>
#    <p> Because {{ __os__name}} compliant systems just work better </p>
#    <p> {{ name }} . RIP </p>
# ''', creator="Gods", more_people="..", **more )
#
# loading pages from external files
# of course, you can send active context to it like above
# invalidpage_404error = temples('404.godsleather')

# When handling a website what do you need?
#           . dynamic templates
#           . forms
#           . static files
#           . control over wsgi-environ
# control over wsgi-environ via lRequest and lResponse objects 
# :Request and :Response methods are all available to :lRequest and :lResponse
from werkzeug.wrappers import Request 
from werkzeug.wrappers import Response 
import os

class lRequest(Request):
    max_content_length = 512 * 1024 * 1024 
    is_multithread = True
    is_multiprocess = True

    __const__ = "lRequest is not thread-local to every function, unlike Flask"

class lResponse(Response):
    default_mimetype = 'text/html'
    __const__ = "Every valid :view function returns type lResponse"

# views are functions that --> lRequest --> lResponse
# what information does your view need to have of your runtime?
# Answer. path and method
# Register path and method attributes to your views

# cached_url conf stores a mapping from urltemplate -> :fixed_attr(function, method, alias)
cached_urlconf = dict()

from collections import namedtuple
fixed_attr = namedtuple('fa', ['function', 'method', 'alias', 'urltemplate'])

class view:
    # register your function with view(function, urltemplate, method, alias(if any))
    # two view functions can never have the same :urltemplate and :method option

    def __init__(self, func, urltemplate, method='GET', alias=None):
        if not func: raise RuntimeError
        self.func = func
        self.rurltemplate = Router(urltemplate)
        self.urltemplate = urltemplate
        self.method = method
        self.alias = alias
        
        if len(cached_urlconf.get(self.urltemplate, [])) > 0:
            t = cached_urlconf[self.urltemplate]
            for _t in t:
                if self.method == _t.method: raise viewerror("err")
            
            cached_urlconf[self.urltemplate].append(fixed_attr(self.func, self.method, self.alias, self.rurltemplate))
            return

        cached_urlconf.update( {self.urltemplate: [fixed_attr(self.func, self.method, self.alias, self.rurltemplate)]})


    def __call__(self):
        return self.func()
    
    @staticmethod
    def reverse(alias):
        for (k, v) in cached_urlconf.items():
            for _v in v:
                if _v.alias == alias:
                    return _v.urltemplate 

        return None

    register = __init__

class godsent:
    # this is the wsgi-callable application
    def __init__(self, urlconf, name=None):
        self.urlconf = urlconf
        self.name = name
    
    def __call__(self, environ, start_response):
        # environ will simply propagate through your view functions
        # a function is invalidated at runtime
        # when it does not return a valid lResponse objects instance
        # at this point, map your url to appropriate view-instance

        self.request = lRequest(environ)
        __view__, ctx = self._inspect_view(self.request.path, self.request.method)

        if __view__ is None: raise RuntimeError('404 HTTP Error')
        rview = __view__(self.request, ctx)
        return rview(environ, start_response)

    def _inspect_view(self, path, method):
        for (k, v) in self.urlconf.items():
            for items in v:
                rule = items.urltemplate
                rule = rule(path)

                if rule not in [None, {}, False]:
                    if items.method == method:
                        return items.function, rule
        return None, None


    def redirect(self, to, method='GET', alias=True):
        # redirect to 'to' reversing 'to' if alias is set
        # redirect should be invoked only at end of your view function
        # as it returns from the point of invocation
        if alias:
            to = view.reverse(to)
            if to is None: return internalerror("Your :alias:to does not match any view function")
            
            for t in self.urlconf[to]:
                    if method == t.method:
                        return lResponse(status=302, headers=[('Location', t.urltemplate)])
        
        return lResponse(status=302, headers=[('Location', to)])

    def __repr__(self):
        __out__ = f':name   {self.name}\n'
        __out__ += ':urlconf' + '\t'
        for (k, v) in cached_urlconf.items():
            for x in v:
                __out__ += f' {k}' + '\n'
                __out__ += f'\t\t-- {x.function}' + '\n'
                __out__ += f'\t\t-- {x.method}' + '\n'
                __out__ += f'\t\t-- {x.alias}' + '\n'
                __out__ += f'\t\t---------------\n\t\t'
        
        return __out__

# uploads are stored in -- matthew
fdir = 'matthew'
import os
os.makedirs(fdir, exist_ok=True)

def __clean__filename(text: str):
        # filename can only have ASCII letters, digits, dashes, underscores(_) and dots(.)
        # whitespaces are replaced by single dash(-). filename are limited to 255 chars
        fname = text.encode('ASCII', 'ignore').decode('ASCII')
        fname = os.path.basename(fname.replace('\\', os.path.sep))
        fname = re.sub(r'[^a-zA-Z0-9-_.\s]', '', fname).strip()
        fname = re.sub(r'[-\s]+', '-', fname).strip('.-')
        return fname[:255] or 'unnamed'

# example
# . form data
# 'request is not an object, name it what you will
# def show(request):
#     return lResponse(form_html, headers=[('Content-Type', 'text/html')])
# 
# def useit(request):
#     name = request.form.get('name', 'anonymous')
#     return lResponse(f"you are {name}")
# 
# 
# aa = view(show, '/submit', 'GET')
# bb = view(useit, '/submit', 'POST')
# 
# form_html = f'''
#     <html>
#         <body>
#             <h1>Submit Your Information</h1>
#             <form method="POST" action="/submit">
#                 <label for="name">Name:</label>
#                 <input type="text" id="name" name="name" required><br><br>
#                 <label for="email">Email:</label>
#                 <input type="email" id="email" name="email" required><br><br>
#                 <button type="submit">Submit</button>
#             </form>
#         </body>
#     </html>
# '''
#
#
# . upload files
# 
# def submit_file(request):
#     return lResponse(file)
# 
# def save_file(request):
#     file = request.files['video']
#     if file.filename == '': return lResponse("No :file selected", status=400)
# 
#     # os.mkdir('uploads', exist_ok=True)
#     filename = os.path.join(fdir, __clean__filename(file.filename))
#     file.save(filename)
#     return lResponse("Video Saved successfully")
# 
# 
# cc = view(submit_file, '/file', 'GET')
# dd = view(save_file, '/file', 'POST')
# 
# file = '''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Upload Video</title>
# </head>
# <body>
#     <h1>Upload Your Video</h1>
#     <form action="/file" method="POST" enctype="multipart/form-data">
#         <label for="video">Choose a video file:</label>
#         <input type="file" id="video" name="video" accept="video/*" required><br><br>
#         <button type="submit">Upload Video</button>
#     </form>
# </body>
# </html>'''
# 

godstemple_t = r'''
<!DOCTYPE html>
<html lang="en">
<%
    if not defined(error_code):
        error_code = "godsend"
%>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> {{ error_code }} </title>
    <style>
        body {
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .container {
            text-align: center;
        }
        h1 {
            margin: 20px 0; /* Double the original margin */
            font-size: 5rem; /* Double the font size */
            letter-spacing: 0.4rem; /* Double the letter spacing */
            text-shadow: 0 4px 10px rgba(0, 0, 0, 0.7); /* Adjust the shadow */
        }
        .lines {
            font-size: 6rem; /* Double the font size */
            color: #f39c12;
            text-shadow: 0 6px 16px rgba(243, 156, 18, 0.8); /* Adjust the shadow */
        }
        .godsend {
            font-size: 8rem; /* Double the font size */
            color: #ecf0f1;
            text-shadow: 0 10px 30px rgba(236, 240, 241, 0.9); /* Adjust the shadow */
            animation: glow 2s infinite;
        }
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 20px #ecf0f1, 0 0 40px #ecf0f1, 0 0 60px #ecf0f1;
            }
            50% {
                text-shadow: 0 0 40px #ffffff, 0 0 80px #ffffff, 0 0 120px #ffffff;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="lines">||||||||||||||||||</h1>
        <h1 class="godsend">GODSEND</h1>
        <h1 class="lines">||||||||||||||||||</h1>
    </div>
</body>
</html>
'''


import sys
__open__pg = temples(godstemple_t, error_code='godsend')

def welcome(request, ctx=None):
    return lResponse(__open__pg, headers=[('Content-Type', 'text/html')])

__welcome__ = view(welcome, '/',  method='GET', alias='welcome')


# now some command line utilities
import argparse
parser = argparse.ArgumentParser(description = "Set config values for Godsend")
parser.add_argument('--debug', type=bool, default=False, help='Turning off debug will just restrict the program to write to stderr')
parser.add_argument('--port', type=int, default=8080)
parser.add_argument('--host', type=str, default='localhost')
args = parser.parse_args()

__write__stderr = args.debug
__port__, __host__ = args.port, args.host

# do not write to errors to the console
if __write__stderr is False: sys.stderr = open(os.devnull, 'w')

def run(app, host=__host__, port=__port__):
    # wsgi applications are service-able on many hosts
    # gunicorn, nginx, and more

    from wsgiref.simple_server import make_server
    __wsgi__server = make_server(host, port, app)

    try: __wsgi__server.serve_forever()
    except: __wsgi__server.close()

app = godsent(cached_urlconf)
run(app)
