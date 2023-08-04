import {task_obj, data_input} from './tasks.js'
export let get_attachments = document.querySelector(".attachment_data").textContent//data will land in a hidden <p>
const attachment_btn = document.querySelector(".attachment_btn")
const table_headers_node = document.querySelectorAll(".files")
export const attach_header_array = [...table_headers_node]
let tbody = document.querySelector(".attachment_body")//For table creation
/*
Remember there are 2 classes like this. the Task and Attachment table contents. 
[0] = task table; [1] = attachment table 
*/
let t_header = document.querySelectorAll(".tbl_header")
let t_content = document.querySelectorAll(".tbl_content")
let row, cell
let data_to_send_obj = { //get attach table
    ID_Proc: '',
    Doc: '',
    Proc:'',//for pdf file
    To_do: '',
}

let post_pdf_obj = { //get pdf file
    Loio_id: '',
    ID_Proc: '',
    Proc: '',
}

let pdf = document.querySelector(".pdf_file")
if(pdf !== null) {
    console.log(`PDF File exists`)
    let pdf_content = pdf.textContent
    var base64regex = /^([0-9a-zA-Z+/]{4})*(([0-9a-zA-Z+/]{2}==)|([0-9a-zA-Z+/]{3}=))?$/;

    //FIXME: FIX THIS
    // let test1 = base64regex.test(String.raw`${pdf_content}`);    
    // console.log(test1)
    // let binary_pdf = ""
    // for(let i = 0; i < pdf_content.length; i++) {
    //     binary_pdf += pdf_content[i].charCodeAt(0).toString(2)+ " "
    // }


    // console.log(binary_pdf)
    
    // let b = new Blob([String.raw`${pdf_content}`], {type: "application/pdf"}) 
    let b = new Blob([pdf_content], {type: "application/pdf"}) 
    // let b = new Blob([String.raw`${pdf_content}`], {type: 'application/msword'}) 
    console.log(b)
    let pdf_url = window.URL.createObjectURL(b)
    console.log(pdf_url)
    let download = document.querySelector(".download")
    download.href = pdf_url
    download.download = "pdf_file" 

    download.click()


    /* var reader = new FileReader();
	reader.onload = function(e) {
		// binary data
        let file_result = e.target.result
		console.log(file_result);
        
        file_result.download = "blob_test"
	};
	reader.onerror = function(e) {
		// error occurred
		console.log('Error : ' + e.type);
	};
	reader.readAsArrayBuffer(b);  */
}
else console.log("Error, no file found")

if (get_attachments !== '' && get_attachments !== "There are one or more missing parameters") {
    var attach_data = JSON.parse(get_attachments)
    load_data_to_table(attach_data)
    const nav_btns = document.querySelectorAll(".li_btn")
    nav_btns[0].addEventListener('click', switch_to_tasks_table)
    nav_btns[1].addEventListener('click', switch_to_attach_table)
}
else {
    console.log("ATTACHMENT parameter missing.")
}

attachment_btn.addEventListener('click', request_attach_data)

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
    show_table()
}

function row_click_listener(current_row) {
    current_row.addEventListener('click', request_file)
}

function request_file() {
    //retrieve session storage item to recall the attachment table
    let request_attach = sessionStorage.getItem("request_attach")//this goes directly into the attach input
    let request_attach_obj = JSON.parse(request_attach)//get data for pdf POST
    let form = document.querySelector(".pdf_form")
    let attach_input = document.querySelector(".request_attach")
    
    post_pdf_obj.Loio_id = this.cells[1].innerHTML //data for wbs
    post_pdf_obj.ID_Proc = request_attach_obj.ID_Proc
    post_pdf_obj.Proc = request_attach_obj.Proc 

    //delete proc for attach request
    delete request_attach_obj.Proc
    let request_attach_after_pdf = JSON.stringify(request_attach_obj) 
    let pdf_input = document.querySelector(".pdf_data_input")
    let pdf_data = JSON.stringify(post_pdf_obj)

    attach_input.value = request_attach_after_pdf
    pdf_input.value = pdf_data
    console.log(`ATTACH REQUEST DATA: ${attach_input.value}`)
    console.log(`PDF REQUEST DATA: ${pdf_data}`)
    form.submit()
}

function request_attach_data() {
    console.log(`requesting the attach table: ${JSON.stringify(task_obj)}`)
    data_to_send_obj.ID_Proc = task_obj.ID_Proc
    data_to_send_obj.Doc = task_obj.Doc
    data_to_send_obj.Proc = task_obj.Proc
    data_to_send_obj.To_do = task_obj.To_do

    //Deleting the mobile view todo div inside ID_PROC
    if(data_to_send_obj.Proc.includes("<div")) {
        console.log("Div is true")
            data_to_send_obj.Proc = data_to_send_obj.Proc.replace(`<div class="to_do_moved"><b>To do</b>: ${task_obj.To_do}</div>`, "")
    }
    delete data_to_send_obj.To_do //delete the reference to send less data

    let json_obj = JSON.stringify(data_to_send_obj)
    data_input[0].value = json_obj
    //store in session
    sessionStorage.setItem("request_attach", json_obj)
}

function show_table() {
    t_header[0].classList.add("hide_element")//tasks = 0
    t_content[0].classList.add("hide_element")
    t_header[1].classList.add("show_element")//attachments = 1
    t_content[1].classList.add("show_element")
    t_header[1].classList.remove("hide_element")
    t_content[1].classList.remove("hide_element")
}

function switch_to_tasks_table() {
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

function switch_to_attach_table(){
    show_table()
    let nav_btns = document.querySelectorAll(".li_btn")   
    if (nav_btns[1].classList.contains("opacity")){
    nav_btns[0].classList.toggle("opacity")//task
    nav_btns[1].classList.toggle("opacity")//attach
    }
}