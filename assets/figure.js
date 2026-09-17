/* ===================================================================
   figure.js — نواة لوحات الرسم في الدروس
   مختبر الجبر الخطي

   لوحة صغيرة بإحداثيات رياضية (الأصل في الوسط، والمحور الصادي لأعلى)،
   تقرأ ألوانها من متغيّرات CSS فتتبع الوضع الداكن، وتضبط مخزنها على
   كثافة الشاشة فلا تبدو ضبابية.

   الاستعمال داخل الدرس:
     var FIG = LinalgFig.FIG, onTheme = LinalgFig.onTheme, plane = LinalgFig.plane;
     var fig = FIG('cvId');
     function draw(){ fig.fit([a, b]).clear(); fig.grid().arrow([0,0], a, fig.col().accent); }
     onTheme(draw); draw();

   يُحمَّل قبل سكربت الدرس، لا بعده — أول رسم يحتاجه جاهزاً.
   =================================================================== */
(function (root) {
  "use strict";

  /* يوحّد مخزن اللوحة مع مقاسها المعروض × كثافة الشاشة، ويضبط تحويل
     السياق فتبقى إحداثيات الرسم بوحدات CSS كما كتبها الدرس. */
  root.LinalgHiDPI = function (cv, ctx) {
    if (!cv) return null;
    var r = cv.getBoundingClientRect();
    var W = Math.round(r.width), H = Math.round(r.height);
    if (!W || !H) return null;
    var dpr = Math.max(1, Math.min(3, root.devicePixelRatio || 1));
    var bw = Math.round(W * dpr), bh = Math.round(H * dpr);
    if (cv.width !== bw || cv.height !== bh) { cv.width = bw; cv.height = bh; }
    (ctx || cv.getContext("2d")).setTransform(dpr, 0, 0, dpr, 0, 0);
    return { W: W, H: H };
  };

  function FIG(id){
    var cv=document.getElementById(id); if(!cv) return null;
    var ctx=cv.getContext('2d'), f={cv:cv,ctx:ctx,W:cv.width,H:cv.height,sc:34,ox:cv.width/2,oy:cv.height/2};
    /* يوحّد مخزن اللوحة مع مقاسها المعروض × كثافة الشاشة فلا تبدو ضبابية */
    f.hidpi=function(){
      var d=window.LinalgHiDPI&&window.LinalgHiDPI(cv,ctx);
      if(d){f.W=d.W;f.H=d.H;}
      return f;};
    function v(n,fb){var c=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return c||fb;}
    f.col=function(){return {paper:v('--paper','#f6f1e7'),ink:v('--ink','#1c1a15'),soft:v('--soft','#6f6757'),
      line:v('--line','#ded4c2'),accent:v('--accent','#0d5c46'),terra:v('--terra','#c2562f'),vio:v('--vio','#5b3f8f')};};
    f.view=function(sc,ox,oy){f.sc=sc;if(ox!=null)f.ox=ox;if(oy!=null)f.oy=oy;return f;};
    /* يضبط المقياس والأصل ليملأ المحتوى اللوحة — والأصل يبقى مرئياً دائماً */
    f.fit=function(pts,pad,maxSc){
      pad=pad==null?34:pad;
      var xs=[0],ys=[0];
      pts.forEach(function(p){ if(p&&isFinite(p[0])&&isFinite(p[1])){xs.push(p[0]);ys.push(p[1]);} });
      var x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs),
          y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
      var w=Math.max(x1-x0,.8), h=Math.max(y1-y0,.8);
      f.sc=Math.min(maxSc||260,(f.W-2*pad)/w,(f.H-2*pad)/h);
      f.ox=f.W/2-((x0+x1)/2)*f.sc;
      f.oy=f.H/2+((y0+y1)/2)*f.sc;
      return f;};
    f.X=function(x){return f.ox+x*f.sc;};
    f.Y=function(y){return f.oy-y*f.sc;};
    f.clear=function(){f.hidpi();var c=f.col();ctx.clearRect(0,0,f.W,f.H);ctx.fillStyle=c.paper;ctx.fillRect(0,0,f.W,f.H);return f;};
    f.grid=function(){
      var c=f.col(),i;ctx.save();ctx.strokeStyle=c.line;ctx.lineWidth=1;
      for(i=Math.ceil(-f.ox/f.sc);f.X(i)<f.W;i++){ctx.beginPath();ctx.moveTo(f.X(i),0);ctx.lineTo(f.X(i),f.H);ctx.stroke();}
      for(i=Math.ceil((f.oy-f.H)/f.sc);f.Y(i)>0;i++){ctx.beginPath();ctx.moveTo(0,f.Y(i));ctx.lineTo(f.W,f.Y(i));ctx.stroke();}
      ctx.strokeStyle=c.ink;ctx.lineWidth=1.6;ctx.globalAlpha=.55;
      ctx.beginPath();ctx.moveTo(0,f.Y(0));ctx.lineTo(f.W,f.Y(0));ctx.stroke();
      ctx.beginPath();ctx.moveTo(f.X(0),0);ctx.lineTo(f.X(0),f.H);ctx.stroke();ctx.restore();return f;};
    f.line=function(a,b,col,w,dash){
      ctx.save();ctx.strokeStyle=col;ctx.lineWidth=w||2;if(dash)ctx.setLineDash(dash);
      ctx.beginPath();ctx.moveTo(f.X(a[0]),f.Y(a[1]));ctx.lineTo(f.X(b[0]),f.Y(b[1]));ctx.stroke();ctx.restore();return f;};
    f.ray=function(d,col,dash){ /* خط لانهائي باتجاه d يمر بالأصل */
      var n=Math.hypot(d[0],d[1]); if(n<1e-9) return f;
      var k=(f.W+f.H)/f.sc;
      return f.line([-d[0]/n*k,-d[1]/n*k],[d[0]/n*k,d[1]/n*k],col,1.8,dash||[7,6]);};
    f.rayAt=function(p,d,col,dash){
      var n=Math.hypot(d[0],d[1]); if(n<1e-9) return f;
      var k=(f.W+f.H)/f.sc, u=[d[0]/n*k,d[1]/n*k];
      return f.line([p[0]-u[0],p[1]-u[1]],[p[0]+u[0],p[1]+u[1]],col,2.2,dash||null);};
    f.arrow=function(a,b,col,w){
      var x1=f.X(a[0]),y1=f.Y(a[1]),x2=f.X(b[0]),y2=f.Y(b[1]),an=Math.atan2(y2-y1,x2-x1),h=9;
      if(Math.hypot(x2-x1,y2-y1)<1.5) return f;
      ctx.save();ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=w||2.6;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
      ctx.beginPath();ctx.moveTo(x2,y2);
      ctx.lineTo(x2-h*Math.cos(an-.42),y2-h*Math.sin(an-.42));
      ctx.lineTo(x2-h*Math.cos(an+.42),y2-h*Math.sin(an+.42));
      ctx.closePath();ctx.fill();ctx.restore();return f;};
    f.dot=function(p,col,r){ctx.save();ctx.fillStyle=col;ctx.beginPath();ctx.arc(f.X(p[0]),f.Y(p[1]),r||4,0,7);ctx.fill();ctx.restore();return f;};
    f.poly=function(pts,stroke,fill,w,dash){
      ctx.save();ctx.beginPath();pts.forEach(function(p,i){i?ctx.lineTo(f.X(p[0]),f.Y(p[1])):ctx.moveTo(f.X(p[0]),f.Y(p[1]));});
      ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill();}
      if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=w||2;if(dash)ctx.setLineDash(dash);ctx.stroke();}ctx.restore();return f;};
    f.circle=function(r,col,w,dash){
      ctx.save();ctx.strokeStyle=col;ctx.lineWidth=w||2;if(dash)ctx.setLineDash(dash);
      ctx.beginPath();ctx.arc(f.X(0),f.Y(0),r*f.sc,0,7);ctx.stroke();ctx.restore();return f;};
    f.arc=function(a0,a1,r,col){
      ctx.save();ctx.strokeStyle=col;ctx.lineWidth=2;ctx.beginPath();
      ctx.arc(f.X(0),f.Y(0),r*f.sc,-a1,-a0);ctx.stroke();ctx.restore();return f;};
    f.right=function(p,d1,d2,col,s){ /* علامة الزاوية القائمة عند p بين اتجاهين */
      var n1=Math.hypot(d1[0],d1[1]),n2=Math.hypot(d2[0],d2[1]); if(n1<1e-9||n2<1e-9) return f;
      s=s||.34;var a=[d1[0]/n1*s,d1[1]/n1*s],b=[d2[0]/n2*s,d2[1]/n2*s];
      ctx.save();ctx.strokeStyle=col;ctx.lineWidth=1.8;ctx.beginPath();
      ctx.moveTo(f.X(p[0]+a[0]),f.Y(p[1]+a[1]));
      ctx.lineTo(f.X(p[0]+a[0]+b[0]),f.Y(p[1]+a[1]+b[1]));
      ctx.lineTo(f.X(p[0]+b[0]),f.Y(p[1]+b[1]));ctx.stroke();ctx.restore();return f;};
    f.tag=function(p,s,col,dx,dy){
      ctx.save();ctx.fillStyle=col;ctx.font='600 13px ui-monospace,Menlo,Consolas,monospace';
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(s,f.X(p[0])+(dx||0),f.Y(p[1])+(dy||0));ctx.restore();return f;};
    f.label=function(p,s,col,d){ /* وسم مزاح بعيداً عن الأصل في اتجاه p — فلا يركب السهم */
      var n=Math.hypot(p[0],p[1])||1, k=(d==null?26:d);
      return f.tag(p,s,col,p[0]/n*k,-p[1]/n*k);};
    f.note=function(px,py,s,col){
      ctx.save();ctx.fillStyle=col;ctx.font='12px ui-monospace,Menlo,Consolas,monospace';
      ctx.textAlign='left';ctx.textBaseline='top';ctx.fillText(s,px,py);ctx.restore();return f;};
    return f;
  }
  /* أعِد الرسم عند تبديل السمة */
  function onTheme(fn){
    new MutationObserver(fn).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
    var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(fn,120);});
  }
  /* المستوى المشترك لمتجهين: يرسم الزاوية الحقيقية بينهما مهما كان بعدهما */
  function plane(a,b){
    var na=Math.hypot.apply(null,a);
    if(na<1e-9) return null;
    var e=a.map(function(v){return v/na;});
    var pb=b.reduce(function(s,v,i){return s+v*e[i];},0);
    var w=b.map(function(v,i){return v-pb*e[i];});
    var nw=Math.hypot.apply(null,w);
    return {A:[na,0], B:[pb,nw], na:na, proj:pb, perp:nw};
  }

  root.LinalgFig = { FIG: FIG, onTheme: onTheme, plane: plane };
})(window);
