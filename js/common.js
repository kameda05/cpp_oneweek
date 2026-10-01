// ===== C++ SYNTAX HIGHLIGHTER =====
var SH_KEYWORDS = new Set([
  'namespace','using','class','struct','union','enum','template','typename',
  'public','private','protected','friend','virtual','override','final',
  'static','const','constexpr','volatile','mutable','inline','extern','explicit',
  'new','delete','return','if','else','for','while','do','switch','case',
  'break','continue','default','goto','try','catch','throw','noexcept',
  'this','operator','sizeof','typedef','true','false','nullptr','NULL',
  'static_cast','dynamic_cast','const_cast','reinterpret_cast','typeid'
]);

var SH_TYPES = new Set([
  'int','char','bool','double','float','long','short','signed','unsigned',
  'void','auto','size_t','wchar_t',
  'std','string','cout','cin','cerr','endl','vector','list','map','set',
  'multimap','multiset','stack','queue','deque','pair','iterator','const_iterator',
  'ifstream','ofstream','fstream','istream','ostream','stringstream'
]);

function shEsc(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function shSpan(cls, s) {
  return '<span class="' + cls + '">' + shEsc(s) + '</span>';
}

function highlightCpp(code) {
  var result = '';
  var i = 0;
  var n = code.length;
  var lineStart = true;

  while (i < n) {
    var c = code[i];

    // Preprocessor directive (#include, #define, ...)
    if (c === '#' && lineStart) {
      var e = code.indexOf('\n', i);
      if (e === -1) e = n;
      var line = code.slice(i, e);
      var m = line.match(/^(#\s*\w+)(\s*)(.*)$/);
      if (m) {
        result += shSpan('sh-preproc', m[1]) + shEsc(m[2]);
        var rest = m[3];
        var cm = rest.indexOf('//');
        var body = cm === -1 ? rest : rest.slice(0, cm);
        var tail = cm === -1 ? '' : rest.slice(cm);
        result += /^[<"]/.test(body) ? shSpan('sh-string', body) : shEsc(body);
        if (tail) result += shSpan('sh-comment', tail);
      } else {
        result += shSpan('sh-preproc', line);
      }
      i = e;
      continue;
    }

    if (c === '\n') { lineStart = true; result += c; i++; continue; }
    if (c !== ' ' && c !== '\t') lineStart = false;

    // Line comment //
    if (c === '/' && i + 1 < n && code[i+1] === '/') {
      var e = code.indexOf('\n', i);
      if (e === -1) e = n;
      result += shSpan('sh-comment', code.slice(i, e));
      i = e;
      continue;
    }

    // Block comment /* */
    if (c === '/' && i + 1 < n && code[i+1] === '*') {
      var e = code.indexOf('*/', i + 2);
      if (e === -1) e = n; else e += 2;
      result += shSpan('sh-comment', code.slice(i, e));
      i = e;
      continue;
    }

    // String / char literal
    if (c === '"' || c === "'") {
      var j = i + 1;
      while (j < n && code[j] !== '\n') {
        if (code[j] === '\\') { j += 2; continue; }
        if (code[j] === c) { j++; break; }
        j++;
      }
      result += shSpan('sh-string', code.slice(i, j));
      i = j;
      continue;
    }

    // Number (not preceded by identifier char)
    if (/\d/.test(c) && (i === 0 || !/[a-zA-Z0-9_]/.test(code[i-1]))) {
      var j = i;
      while (j < n && /[0-9a-fA-FxX.uUlLfF]/.test(code[j])) j++;
      result += shSpan('sh-number', code.slice(i, j));
      i = j;
      continue;
    }

    // Identifier / keyword / type
    if (/[a-zA-Z_]/.test(c)) {
      var j = i;
      while (j < n && /[a-zA-Z0-9_]/.test(code[j])) j++;
      var word = code.slice(i, j);

      if (SH_KEYWORDS.has(word)) {
        result += shSpan('sh-keyword', word);
      } else if (SH_TYPES.has(word)) {
        result += shSpan('sh-type', word);
      } else if (/^[A-Z][a-z]/.test(word)) {
        result += shSpan('sh-typename', word);
      } else {
        result += shEsc(word);
      }
      i = j;
      continue;
    }

    // Everything else (operators, punctuation, whitespace)
    result += shEsc(c);
    i++;
  }

  return result;
}

// ===== MAIN: HIGHLIGHT + LINE NUMBERS + COPY BUTTON =====
document.querySelectorAll('pre:not(.terminal)').forEach(function(pre) {
  var original = pre.textContent;

  // Apply syntax highlighting
  pre.innerHTML = highlightCpp(original);

  // Add line numbers
  var lines = pre.innerHTML.split('\n');
  if (lines[lines.length - 1].trim() === '') lines.pop();
  pre.innerHTML = lines.map(function(line, i) {
    return '<span class="line-num">' + (i + 1) + '</span>' + line;
  }).join('\n');

  // Wrap with copy button
  var wrap = document.createElement('div');
  wrap.className = 'pre-wrap';
  pre.parentNode.insertBefore(wrap, pre);
  wrap.appendChild(pre);

  var btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'コピー';
  btn.addEventListener('click', function() {
    navigator.clipboard.writeText(original.trim()).then(function() {
      btn.textContent = 'コピー完了!';
      btn.classList.add('copied');
      setTimeout(function() { btn.textContent = 'コピー'; btn.classList.remove('copied'); }, 2000);
    });
  });
  wrap.appendChild(btn);
});
