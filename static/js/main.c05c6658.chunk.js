(this["webpackJsonpblockchain-fe"]=this["webpackJsonpblockchain-fe"]||[]).push([[0],{10:function(e,t,c){},12:function(e,t,c){"use strict";c.r(t);var n=c(1),l=c.n(n),s=c(4),a=c.n(s),r=(c(9),c(2)),b=(c(10),c(0));var i=function(e){var t=Object(n.useState)([]),c=Object(r.a)(t,2),l=c[0],s=c[1];return Object(b.jsxs)(b.Fragment,{children:[Object(b.jsx)("div",{onClick:function(){console.log(e.user),fetch("http://localhost:5000/parse_transactions/".concat(e.user)).then((function(e){return e.json()})).then((function(e){return s(e.transactions)}))},children:"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0442\u0430\u0434\u0438\u0438"}),Object(b.jsxs)("table",{children:[Object(b.jsx)("thead",{className:"u-black u-table-header u-table-header-1",children:Object(b.jsxs)("tr",{children:[Object(b.jsx)("th",{className:"u-table-cell",children:"\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c"})]})}),l.map((function(e){return Object(b.jsxs)("tr",{children:[Object(b.jsx)("td",{className:"u-table-cell",children:e.message}),Object(b.jsx)("td",{className:"u-table-cell",children:e.receiver}),Object(b.jsx)("td",{className:"u-table-cell",children:e.sender})]})}))]})]})};var j=function(){var e=Object(n.useState)([]),t=Object(r.a)(e,2),c=t[0],l=t[1];Object(n.useEffect)((function(){s()}),[]);var s=function(){fetch("http://localhost:5000/parse_signatures").then((function(e){return e.json()})).then((function(e){return l(e.signatures)}))};return Object(b.jsxs)(b.Fragment,{children:[Object(b.jsx)("thead",{className:"u-black u-table-header u-table-header-1",children:Object(b.jsxs)("tr",{children:[Object(b.jsx)("th",{className:"u-table-cell",children:"\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440"}),Object(b.jsx)("th",{className:"u-table-cell",children:"\u041f\u043e\u043b\u0435 \u0434\u0430\u043d\u043d\u044b\u0445"})]})}),Object(b.jsx)("tbody",{className:"u-table-alt-palette-1-light-3 u-table-body",children:c.map((function(e){return Object(b.jsxs)("tr",{children:[Object(b.jsx)("td",{className:"u-table-cell",children:e}),Object(b.jsx)("td",{className:"u-table-cell",children:Object(b.jsx)(i,{user:e})})]})}))})]})},u=function(e){e&&e instanceof Function&&c.e(3).then(c.bind(null,13)).then((function(t){var c=t.getCLS,n=t.getFID,l=t.getFCP,s=t.getLCP,a=t.getTTFB;c(e),n(e),l(e),s(e),a(e)}))};a.a.render(Object(b.jsx)(l.a.StrictMode,{children:Object(b.jsx)(j,{})}),document.getElementById("root")),u()},9:function(e,t,c){}},[[12,1,2]]]);
//# sourceMappingURL=main.c05c6658.chunk.js.map