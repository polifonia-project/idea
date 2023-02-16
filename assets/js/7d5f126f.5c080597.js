"use strict";(self.webpackChunkidea_dashboard=self.webpackChunkidea_dashboard||[]).push([[742],{3905:(e,t,n)=>{n.d(t,{Zo:()=>l,kt:()=>u});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var c=r.createContext({}),p=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},l=function(e){var t=p(e.components);return r.createElement(c.Provider,{value:t},e.children)},d="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,c=e.parentName,l=s(e,["components","mdxType","originalType","parentName"]),d=p(n),f=o,u=d["".concat(c,".").concat(f)]||d[f]||m[f]||i;return n?r.createElement(u,a(a({ref:t},l),{},{components:n})):r.createElement(u,a({ref:t},l))}));function u(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=f;var s={};for(var c in t)hasOwnProperty.call(t,c)&&(s[c]=t[c]);s.originalType=e,s[d]="string"==typeof e?e:o,a[1]=s;for(var p=2;p<i;p++)a[p]=n[p];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},8458:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>a,default:()=>m,frontMatter:()=>i,metadata:()=>s,toc:()=>p});var r=n(7462),o=(n(7294),n(3905));const i={sidebar_position:3},a="PolifoniaCQ Embeddings",s={unversionedId:"competency-questions/polifoniacq-embeddings",id:"competency-questions/polifoniacq-embeddings",title:"PolifoniaCQ Embeddings",description:"To enable search, similarity, and analysis of the PolifoniaCQ dataset, we computed sentence-level embeddings from each competency question. This is done using the SentenceTransformers, a library registered to HuggingFace providing for state-of-the-art sentence, text embeddings.",source:"@site/docs/competency-questions/polifoniacq-embeddings.mdx",sourceDirName:"competency-questions",slug:"/competency-questions/polifoniacq-embeddings",permalink:"/idea/competency-questions/polifoniacq-embeddings",draft:!1,editUrl:"https://github.com/polifonia-project/idea/dashboard/docs/competency-questions/polifoniacq-embeddings.mdx",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"Problematic CQs",permalink:"/idea/competency-questions/problematic-cqs"}},c={},p=[],l={toc:p},d="wrapper";function m(e){let{components:t,...i}=e;return(0,o.kt)(d,(0,r.Z)({},l,i,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"polifoniacq-embeddings"},"PolifoniaCQ Embeddings"),(0,o.kt)("p",null,"To enable search, similarity, and analysis of the PolifoniaCQ dataset, we computed sentence-level embeddings from each competency question. This is done using the ",(0,o.kt)("a",{parentName:"p",href:"https://www.sbert.net"},"SentenceTransformers"),", a library registered to ",(0,o.kt)("a",{parentName:"p",href:"https://huggingface.co"},"HuggingFace")," providing for state-of-the-art sentence, text embeddings."),(0,o.kt)("p",null,"The PolifoniaCQ embeddings can be downloaded from ",(0,o.kt)("a",{parentName:"p",href:"https://github.com/polifonia-project/idea/tree/main/data/projections/00000/PolifoniaCQ"},"our repository"),"."),(0,o.kt)("blockquote",null,(0,o.kt)("p",{parentName:"blockquote"},"\u2728 An interactive visualisation of the PolifoniaCQ embeddings is available from a live Tensorboard instance at ",(0,o.kt)("a",{parentName:"p",href:"https://projector.tensorflow.org/?config=https://raw.githubusercontent.com/polifonia-project/idea/main/data/projections/projector_config.json"},"this link"),". From the left panel, make sure to select the ",(0,o.kt)("em",{parentName:"p"},"persona")," tag from the ",(0,o.kt)("em",{parentName:"p"},"label dropdown"),".")),(0,o.kt)("p",null,(0,o.kt)("img",{alt:"Example banner",src:n(6532).Z,width:"2216",height:"1154"})))}m.isMDXComponent=!0},6532:(e,t,n)=>{n.d(t,{Z:()=>r});const r=n.p+"assets/images/cq_embeddings-6035d5c2972c83c3ee5d586ae6b3549b.png"}}]);