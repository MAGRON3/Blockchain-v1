(this["webpackJsonpblockchain-fe"]=this["webpackJsonpblockchain-fe"]||[]).push([[0],{10:function(e,t,c){},12:function(e,t,c){"use strict";c.r(t);var l=c(1),s=c.n(l),n=c(4),a=c.n(n),r=(c(9),c(2)),b=(c(10),c(0));var j=function(e){var t=Object(l.useState)([]),c=Object(r.a)(t,2),s=c[0],n=c[1];return Object(b.jsxs)(b.Fragment,{children:[Object(b.jsx)("div",{onClick:function(){console.log(e.user),fetch("http://localhost:5000/parse_transactions/".concat(e.user)).then((function(e){return e.json()})).then((function(e){return n(e.transactions)}))},children:"\u0421\u0442\u0430\u0434\u0438\u0438"}),Object(b.jsxs)("table",{className:"u-table-entity u-table-entity-1",children:[Object(b.jsx)("thead",{className:"u-black u-table-header u-table-header-1",children:Object(b.jsxs)("tr",{children:[Object(b.jsx)("th",{className:"u-table-cell",children:"\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c"})]})}),s.map((function(e){return Object(b.jsxs)("tr",{children:[Object(b.jsx)("td",{className:"u-table-cell",children:e.message}),Object(b.jsx)("td",{className:"u-table-cell",children:e.receiver}),Object(b.jsx)("td",{className:"u-table-cell",children:e.sender})]})}))]})]})};var i=function(){var e=Object(l.useState)([]),t=Object(r.a)(e,2),c=t[0],s=t[1];return Object(b.jsxs)(b.Fragment,{children:[Object(b.jsx)("button",{onClick:function(){fetch("http://localhost:5000/parse_signatures").then((function(e){return e.json()})).then((function(e){return s(e.signatures)}))},children:"Get users"}),Object(b.jsx)("button",{onClick:function(){s([])},children:"set users"}),Object(b.jsx)("thead",{className:"u-black u-table-header u-table-header-1",children:Object(b.jsxs)("tr",{children:[Object(b.jsx)("th",{className:"u-table-cell",children:"Signature"}),Object(b.jsx)("th",{className:"u-table-cell",children:" \u043d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u0426\u0435\u043d\u0430"})]})}),Object(b.jsxs)("tbody",{className:"u-table-alt-palette-1-light-3 u-table-body",children:[c.map((function(e){return Object(b.jsxs)("tr",{children:[Object(b.jsx)("td",{className:"u-table-cell",children:e}),Object(b.jsx)("td",{className:"u-table-cell",children:Object(b.jsx)(j,{user:e})})]})})),Object(b.jsxs)("tr",{children:[Object(b.jsx)("td",{className:"u-table-cell",children:"\u043e\u0434\u0438\u043d"}),Object(b.jsx)("td",{className:"u-table-cell",children:Object(b.jsx)(j,{})})]})]})]})},u=function(e){e&&e instanceof Function&&c.e(3).then(c.bind(null,13)).then((function(t){var c=t.getCLS,l=t.getFID,s=t.getFCP,n=t.getLCP,a=t.getTTFB;c(e),l(e),s(e),n(e),a(e)}))};a.a.render(Object(b.jsx)(s.a.StrictMode,{children:Object(b.jsx)(i,{})}),document.getElementById("root")),u()},9:function(e,t,c){}},[[12,1,2]]]);
//# sourceMappingURL=main.983fd1ed.chunk.js.map