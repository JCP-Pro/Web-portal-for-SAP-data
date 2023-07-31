import {task_obj, data_input, show_elements} from './tasks.js'
let get_data = document.querySelector(".attachment_data").textContent//data will land in a hidden <p>
let attach_data = JSON.parse(get_data)
const attachment_btn = document.querySelector(".attachment_btn")
let tbody = document.querySelector(".attachment_body")//For table creation
let t_header = document.querySelectorAll(".tbl_header")
let t_content = document.querySelectorAll(".tbl_content")//Remember there are 2 classes like this. the Task and Attachment table contents.
let row, cell
console.log(`This is the get_data: ${get_data}`)
let data_to_send_obj = {
    ID_Proc: '',
    Doc: '',
}

let attach_obj = {
    Loio_id: '',
}

//TODO: MAKE A NAV_BAR WITH ICONS TO GO IN BETWEEN TASK AND FILES REQUESTED(ASK IF THAT'S OK).

load_data_to_table(attach_data)

attachment_btn.addEventListener('click', send_attach_data)

function load_data_to_table(data) {
    for (let i in data) {
        row= tbody.insertRow()
        row.id = i
        cell = row.insertCell()
        cell.classList.add("description")
        cell.textContent = data[i].Descript
        cell = row.insertCell()
        cell.classList.add("loio_id")
        cell.textContent = data[i].Loio_id
        cell = row.insertCell()
        cell.classList.add("comp_id")
        cell.textContent = data[i].Comp_id
        row_click_listener(row)
    }

    show_table()
}

function row_click_listener(current_row) {
    current_row.addEventListener('click', open_file)
}

function open_file() {
    //TODO: Send Loio_id as webservice data to request the pdf file.
    attach_obj.Loio_id = this.cells[1].innerHTML //data for wbs    
}

function send_attach_data() {
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