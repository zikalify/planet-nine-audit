const assert=require('node:assert/strict');
const {audit,flagCount,joint}=require('../docs/site/app.js');
assert.equal(flagCount([0,1,2]),78260);assert.equal(flagCount([]),0);assert.equal(flagCount([0]),56173);assert.equal(flagCount([1]),10187);assert.equal(flagCount([2]),68745);assert.equal(Object.values(joint).reduce((a,b)=>a+b),100000);
let r=audit(['archive-a','archive-b'],false);assert.ok(Math.abs(r.coverage.broad.lower-.35)<1e-12);assert.equal(r.rank[0].name,'south-field');assert.equal(r.rank[0].worst,.1575);
r=audit([],false);assert.equal(r.coverage.narrow.lower,0);assert.equal(r.coverage.broad.upper,0);
r=audit(['archive-a','archive-b'],true);assert.equal(r.coverage.broad.lower,r.coverage.broad.upper);
for(const sel of [[],['archive-a'],['archive-b'],['archive-a','archive-b']])for(const ind of [true,false])for(const v of Object.values(audit(sel,ind).coverage)){assert.ok(v.lower>=0&&v.upper<=1&&v.lower<=v.upper)}
console.log('Site arithmetic and flags: all assertions passed.');
