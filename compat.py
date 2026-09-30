import re
def compat(t):
    # 1. Fjern CSS-variabler: sett inn verdiene direkte (eldre nettlesere kjenner ikke var())
    root=re.search(r":root\{([^}]*)\}",t).group(1)
    vals=dict(re.findall(r"--([\w-]+):([^;]+)",root))
    t=re.sub(r"var\(--([\w-]+)\)",lambda m:vals.get(m.group(1),"inherit"),t)
    # 2. Object.entries finnes ikke i eldre nettlesere
    t=t.replace("Object.entries(m)","Object.keys(m).map(function(k){return [k,m[k]]})")
    # 3. Skriftstørrelse settes også med JS (min() støttes ikke overalt)
    boot=("<script>(function(){function f(){var s=Math.min(window.innerWidth/1920,window.innerHeight/1080)*16;"
          "document.documentElement.style.fontSize=s+'px'}f();window.addEventListener('resize',f);"
          "window.onerror=function(m,u,l){var d=document.createElement('div');"
          "d.style.cssText='position:fixed;left:0;right:0;bottom:0;background:#900;color:#fff;font:20px sans-serif;padding:12px;z-index:9';"
          "d.textContent='Feil: '+m+' (linje '+l+')';document.body.appendChild(d)}})();</script>")
    t=t.replace("<header>",boot+"<header>",1)
    return t
