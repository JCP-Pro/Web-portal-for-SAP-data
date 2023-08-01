import {task_obj, data_input, data_to_send} from './tasks.js'
let get_data = document.querySelector(".attachment_data").textContent//data will land in a hidden <p>
const attachment_btn = document.querySelector(".attachment_btn")
const table_headers_node = document.querySelectorAll(".files")
export const attach_header_array = [...table_headers_node]
let tbody = document.querySelector(".attachment_body")//For table creation
let t_header = document.querySelectorAll(".tbl_header")
let t_content = document.querySelectorAll(".tbl_content")//Remember there are 2 classes like this. the Task and Attachment table contents.
let row, cell
let data_to_send_obj = { //get attach table
    ID_Proc: '',
    Doc: '',
}

let attach_obj = { //get pdf file
    Loio_id: '',
}

if (get_data !== '') {
    var attach_data = JSON.parse(get_data)
    load_data_to_table(attach_data)
    const nav_btns = document.querySelectorAll(".li_btn")
    nav_btns[0].addEventListener('click', load_tasks)
    nav_btns[1].addEventListener('click', load_attach)
}

attachment_btn.addEventListener('click', send_attach_data)

function load_data_to_table(data) {
    for (let i in data) {
        row= tbody.insertRow()
        row.id = i
        let tabindex = parseInt(i) + 3
        row.setAttribute("tabindex", String(tabindex))
        row.classList.add("row")
        cell = row.insertCell()
        cell.classList.add("description")
        cell.classList.add("responsive_cell")
        cell.textContent = data[i].Descript
        cell = row.insertCell()
        cell.classList.add("loio_id")
        cell.classList.add("responsive_cell")
        cell.textContent = data[i].Loio_id
        cell = row.insertCell()
        cell.classList.add("comp_id")
        cell.classList.add("responsive_cell")
        cell.textContent = data[i].Comp_id
        row_click_listener(row)
    }
    console.log(document.querySelectorAll("row"))
    show_table()
}

function row_click_listener(current_row) {
    current_row.addEventListener('click', open_file)
}

function open_file() {
    let form = document.querySelector(".pdf_form")
    attach_obj.Loio_id = this.cells[1].innerHTML //data for wbs
    let pdf_input = document.querySelector(".pdf_data_input")
    let pdf_data = JSON.stringify(attach_obj)
    pdf_input.value = pdf_data
    let pdf_submit = form.querySelector('input[name="data"]')
    console.log(`This is the pdf_submit: ${pdf_submit.value}`)
    form.submit()
}

function send_attach_data() {
    console.log(`requesting the attach table: ${JSON.stringify(task_obj)}`)
    data_to_send_obj.ID_Proc = task_obj.ID_Proc
    data_to_send_obj.Doc = task_obj.Doc

    let json_obj = JSON.stringify(data_to_send_obj)
    data_input[0].value = json_obj
}

function show_table() {
    t_header[0].classList.add("hide_element")
    t_content[0].classList.add("hide_element")
    t_header[1].classList.add("show_element")
    t_content[1].classList.add("show_element")
    t_header[1].classList.remove("hide_element")
    t_content[1].classList.remove("hide_element")
}

function load_tasks() {
    t_header[0].classList.remove("hide_element")
    t_content[0].classList.remove("hide_element")
    t_header[1].classList.remove("show_element")
    t_content[1].classList.remove("show_element")
    t_header[1].classList.add("hide_element")
    t_content[1].classList.add("hide_element")
    let nav_btns = document.querySelectorAll(".li_btn")
    if(nav_btns[0].classList.contains("opacity")) {
        nav_btns[0].classList.toggle("opacity")//task
        nav_btns[1].classList.toggle("opacity")//atta
    }
}

function load_attach() {
    show_table()
    let nav_btns = document.querySelectorAll(".li_btn")   
    if (nav_btns[1].classList.contains("opacity")){
    nav_btns[0].classList.toggle("opacity")//task
    nav_btns[1].classList.toggle("opacity")//attach
    }
}