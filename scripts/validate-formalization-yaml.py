import json,sys,os,yaml
YML=sys.argv[1] if len(sys.argv)>1 else '/home/chris/Github/uniform-sheafy-tate-domains-lean/formalization.yaml'
HERE=os.path.dirname(os.path.abspath(__file__))
d=yaml.safe_load(open(YML))
arx=json.load(open(os.path.join(HERE,'arxiv.json'))); msc=json.load(open(os.path.join(HERE,'msc.json')))
ok=True
def chk(cond,msg):
    global ok
    print(("  OK   " if cond else "  FAIL ")+msg)
    if not cond: ok=False
print("Palomar mechanical checks on", YML)
p=d.get('project',{})
chk(isinstance(p.get('name'),str) and p['name'].strip(), "project.name nonempty")
desc=p.get('description','')
chk(isinstance(desc,str) and desc.strip() and len(desc)<=10000, f"project.description nonempty, <=10000 (len={len(desc)})")
a=p.get('authors')
chk(isinstance(a,list) and a and all(isinstance(x,str) and x.strip() for x in a), "project.authors nonempty list of strings")
rm=p.get('responsible_maintainers')
chk(isinstance(rm,list) and rm and all(isinstance(x,str) and x.strip() for x in rm), "project.responsible_maintainers nonempty list of strings")
chk(p.get('license')=="Apache-2.0", "project.license == Apache-2.0 (matches LICENSE)")
c=d.get('classification',{})
ax=c.get('arxiv',[])
chk(isinstance(ax,list) and 1<=len(ax)<=2 and len(set(ax))==len(ax) and all(x in arx for x in ax), f"classification.arxiv 1-2 distinct valid {ax}")
ms=c.get('msc2020',[])
bad=[x for x in ms if x not in msc]
chk(isinstance(ms,list) and 1<=len(ms)<=8 and len(set(ms))==len(ms) and not bad, f"classification.msc2020 1-8 distinct valid {ms}"+(f" BAD={bad}" if bad else ""))
srcs=d.get('sources',[])
REL={'formalizes','adapts','independently-proves','background','other'}
TYP={'paper','book','web discussion','folklore','original-proof','other'}
chk(isinstance(srcs,list) and bool(srcs), "sources nonempty")
for i,s in enumerate(srcs):
    chk(isinstance(s.get('title'),str) and s['title'].strip(), f"sources[{i}].title nonempty")
    chk(s.get('relationship') in REL, f"sources[{i}].relationship '{s.get('relationship')}' in vocabulary")
    if 'type' in s: chk(s['type'] in TYP, f"sources[{i}].type '{s['type']}' in vocabulary")
    for j,cb in enumerate(s.get('contributors') or []):
        chk(isinstance(cb.get('name'),str) and cb['name'].strip(), f"sources[{i}].contributors[{j}].name nonempty")
        chk(isinstance(cb.get('role'),str) and 0<len(cb['role'])<=200, f"sources[{i}].contributors[{j}].role <=200 chars")
orig=[s for s in srcs if s.get('type')=='original-proof']
subst=[s for s in srcs if s.get('relationship') in {'formalizes','adapts','independently-proves'}]
if orig: chk(all(s.get('relationship')=='other' for s in orig) and not subst, "ORIGINAL alternative")
else: chk(bool(subst), f"SOURCE-BASED alternative ({len(subst)} substantive) -> result_origin: source-based")
am=d.get('automation',{}).get('methods')
chk(isinstance(am,list) and bool(am) and all(isinstance(m,dict) and str(m.get('method','')).strip() for m in am), "automation.methods nonempty, each has nonempty method")
rs=d.get('review',{}).get('status')
chk(isinstance(rs,str) and rs.strip(), f"review.status nonempty ('{rs}')")
chk('repository' not in d, "repository omitted -> substantive-development")
chk(d.get('version')=='v0.4', f"version == v0.4 (got {d.get('version')})")
sz=os.path.getsize(YML); chk(sz<=256*1024, f"file <= 256 KiB ({sz/1024:.1f} KiB)")
print("\nRESULT:", "ALL PASS" if ok else "FAILURES ABOVE")
sys.exit(0 if ok else 1)
