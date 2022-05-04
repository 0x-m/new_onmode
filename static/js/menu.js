
const menuItemTemplateHTML = ``;
const menuGroupTemplateText = ``;
const listMenuTemplateText = ``;


class MenuItem extends HTMLElement {

    static get observedAttributes(){
        return ['caption', 'link'];
    }

    get caption() {
        return this._caption;
    }

    get link(){
        return this._link;
    }

    set link(value) {
        this.setAttribute('link', value);
    }

    set caption(value) {
        this.setAttribute('caption', value);
    }
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                :host {
                    cursor: pointer;
                }
                #caption {
                    font-size: 0.6rem;
                    padding: 0.8rem;
                    cursor: pointer;
                    display: block;
                    transition: 0.5s all;
                    text-decoration: none;
                    border-bottom: 1px solid #0000ef;
                }
                #caption:hover {
                    background-color: rgba(240,240,240,0.5);
                }
            </style>

            <a href="" id="caption"></a>
        `;
        this.shadowRoot.appendChild(template.content.cloneNode(true));
        this._caption = this.shadowRoot.querySelector('#caption');
    }

    attributeChangedCallback(name, oldval, newval) { 
        if (newval === oldval)
            return;

        switch(name) {
            case 'caption':
                this._caption.textContent = newval;
                break;
            case 'link':
                this._caption.href = newval;
            default:
                return;
        }
    }

}

class MenuItemGroup extends HTMLElement {

    static get observedAttributes() {
        return ['caption', 'show'];
    }

    get show() {
        return this.hasAttribute('show');
    }

    set show(value) {
        const pr = Boolean(value);
        if (value) {
            this.setAttribute('show');
        }
        else {
            this.removeAttribute('show');
        }
    }
    get caption() {
        return (this.hasAttribute('caption') ? this.getAttribute('caption') : undefined);
    }

    set caption(value) {
        if (value) {
            this.setAttribute('caption', value);
        }
        else{
            this.removeAttribute('caption');
        }
        
    }
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                :host {
                    cursor: pointer;
                    display:block;
                }
               
                #container {
                    display: flex;
                    flex-direction: column;
                  
                }
              
                #items {
                    display: none;
                    flex-direction:column
                }
                #caption {
                    padding: 0.8rem;
                    font-size: 0.6rem;
                    user-select: none;
                    pointer-events: none;
                    display: block;
                    flex: 90%;
                }
               
              
                #header {
                    display: flex;
                    align-items: center;
                    transition: 0.5s all;
                    border-bottom: 1px solid #efefef;
                }
                #header:hover {
                    background-color: rgba(240,240,240,0.5) !important;
                    
                }
                #arrow {
                    font-size: 0.6rem;
                   
                    padding: 0.4rem;
                }
            </style>

            <div id="header">
                <span id="caption"></span>
                <span id="arrow">&#10095;</span>
            </div>
            

            <div id="container">
                <section id="items">
                    <slot></slot>
                </section>
            </div>
        
        `;

        this.shadowRoot.appendChild(template.content.cloneNode(true));
        this._caption = this.shadowRoot.querySelector('#caption');

    }

    _toggleShow() {
        const disp = this.shadowRoot.querySelector('#items');
        disp.style.display = disp.style.display == 'none' ? 'flex': 'none';
    }

    attributeChangedCallback(name, oldval, newval) {
        if ( newval === oldval) 
            return;
        switch(name) {
            case 'caption' :
                this._caption.textContent = newval;
                break;
            case 'show':
                this.querySelector('#items')
            default:
                return;
        }
    }


}

class ListMenu extends HTMLElement {
    static get observedAttributes() {
        return ['caption']
    }

    get caption() {
        return this.getAttribute('caption');
    }

    set caption(value){
        return this.setAttribute('caption', value);
    }
    constructor() {
        super();

        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                #container {
                    display: flex;
                    flex-direction: column;
                    
                }
                #main {
                    display: flex;
                    flex-direction: column;
                    transform-origin: center center;
                }
                #caption {
                    flex: 80%;
                    color: blue;
                    font-size: 0.6rem;
                    display: block;
                    
                    margin: 2px;
                    cursor: pointer;
                    padding: 0.6rem;
                }
                #header:hover {
                    background-color: rgba(240,240,240,0.5);

                }
                #header{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border-bottom: 1px solid #efefef;
                    user-select: none;
                    display: none;
                }
              #arrow{
                  font-size: 0.7rem;
                  color: gray;
                  pointer-events: none;
                  padding: 0.4rem
              }
            </style>
            
            <div id="container">
                <div id="header">
                    <span id="caption"></span>
                    <span id="arrow">&#10095;</span>
                </div>
                <section id="main">
                    <slot></slot>
                </section>
            </div>
        `;

        this.attachShadow({ mode: 'open' });
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._history = new Array();
        const cont = document.createElement('div');
        cont.innerHTML = this.innerHTML;
        this._main = this.shadowRoot.querySelector('#main');
        this._caption = this.shadowRoot.querySelector('#caption');
        this._prevMenu = this._prevMenu.bind(this);
        this._updateView = this._updateView.bind(this);
        this.addEventListener('click', this._handleClick);
        this._caption.addEventListener('click', this._prevMenu);
        this._default_header = undefined;
        
        

    }

    connecteCallback() {
        
    }
    attributeChangedCallback(name, oldval, newval) {
        if (name == 'caption') {
            if (this._default_header == undefined){
                this._default_header = newval;
            }
            this._caption.textContent = newval;
            console.log('list menu caption changed');
        }
    }
    _allGroups() {
        return Array.from(this.querySelector('menu-group'));
    }
    _updateView(menu) {
       
        this.shadowRoot.querySelector('#main').animate(
            [
                {transform: 'translateX(100px)'},
                {transform: 'translateX(0)'}
            ],
            {
                duration: 300,
                easing: 'ease-in-out'
            }
        )
   
        const obj = document.createElement('menu-group');
        obj.setAttribute('caption', this.caption);
        obj.innerHTML = this.innerHTML;
        this._history.push(obj);
        this.innerHTML = menu.innerHTML;
        this.setAttribute('caption', 'بازگشت');
        if (this._history.length >= 1) {
            this.shadowRoot.querySelector("#header").style.display = "flex";
        }

        
    }

    _handleClick(e) {
        console.log('handle click----------');
        console.log(e.target.tagName);
        if(e.target.tagName.toLowerCase() == 'menu-group'){
            
            this._updateView(e.target);
        }
    }
    
    _prevMenu(){
        const length = this._history.length;
        if(length > 0) {

            this.shadowRoot.querySelector('#main').animate(
                [
                    {transform: 'translateX(-100px)'},
                    {transform: 'translateX(0)'}
                ],
                {
                    duration: 300,
                    easing: 'ease-in-out'
                }
            )
            const prev = this._history.pop()
            console.log(prev);
            this.innerHTML = prev.innerHTML;
            if (length == 1){
                this.shadowRoot.querySelector('#header').style.display = "none";
            }
            //this.setAttribute('caption', prev.caption);
         
        }
    }
}

customElements.define('menu-item', MenuItem);
customElements.define('menu-group', MenuItemGroup);
customElements.define('list-menu', ListMenu);
