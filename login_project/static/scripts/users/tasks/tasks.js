const user_wf = document.querySelector('.user_wf').textContent
const task_array_json = document.querySelector(".task_array").textContent
const task_array = JSON.parse(task_array_json)

//Diaolog buttons
const task_dialog = document.querySelector(".task_dialog")
const close_dialog_icon = document.querySelector(".exit_dialog_container")
const confirm_btn = document.querySelector(".confirm_btn")
const decline_btn = document.querySelector(".decline_btn")
//Diaolog task description
const open_task = document.querySelector(".current_task")
// const data_input = document.querySelector(".data_input") //Probably gonna have a id so change to #id_data
export const data_input = document.querySelectorAll("#id_data")
data_input.forEach((e) => e.setAttribute('hidden', '')) //Hiding the input fields which sends data. 
// data_input[0] is for hiding ATTACH INPUT
let tbody = document.querySelector(".task_body")
let row, cell

//responsive table
let show_elements_array = []


//Task_obj for sending data
export const task_obj = {
    ID_Proc:"",
    Proc:"",
    Task:"",
    Role:"",
    Doc:"",
    To_do:"",
    Imp:"",
    Um: "",
    Dt: "",
}

const data_to_send = {
    ID_Proc: "",
    Task: "",
    Flag: "",
    User_wf: user_wf,
}

//debug purpose
//let task_data = []

load_data_to_table(task_array)

function load_data_to_table(data) {
    for (let i = 0; i < data.length; i++) {
        /* To test in the console use ->
        task_data.push(data[i]) 
        then in the console tryout
        task_data[0].
        Available properties will show up
        */
        row = tbody.insertRow()
        row.id = i //setting id to each row
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("id_proc")
        cell.textContent = data[i].ID_Proc
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("proc")
        cell.textContent = data[i].Proc
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("task")
        cell.textContent = data[i].Task
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("role")
        cell.textContent = data[i].Role
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("doc")
        cell.textContent = data[i].Doc
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("to_do")
        cell.textContent = data[i].To_do
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("imp")
        cell.textContent = data[i].Imp.trim()
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("val")
        cell.textContent = data[i].Um
        cell = row.insertCell()
        cell.classList.add("cell")
        cell.classList.add("dt")
        cell.textContent = data[i].Dt
        task_click_listener(row)
    }
}

function task_click_listener(current_task) {
    current_task.addEventListener('click', task_operation)
}



function task_operation() {
    const content_table = document.querySelector(".task_table")

    //Get data and Insert into task_obj
    for (let i in content_table.rows) {
        
        if (`${i}` === `${this.id}`) {
            const selected_row = content_table.rows[i]
            let id_process = selected_row.cells[0].innerHTML
            let process = selected_row.cells[1].innerHTML
            let task = selected_row.cells[2].innerHTML
            let role = selected_row.cells[3].innerHTML
            let doc = selected_row.cells[4].innerHTML
            let to_do = selected_row.cells[5].innerHTML
            let imp = selected_row.cells[6].innerHTML
            let um = selected_row.cells[7].innerHTML
            let dt = selected_row.cells[8].innerHTML


            task_obj.ID_Proc = id_process
            task_obj.Proc = process
            task_obj.Task = task
            task_obj.Role = role
            task_obj.Doc = doc
            task_obj.To_do = to_do
            task_obj.Imp = imp
            task_obj.Um = um
            task_obj.Dt = dt
            break
        }
    }

    show_dialog()
}

function show_dialog() {
    task_dialog.show()

    if(window.innerWidth < 768) {
        let task_to_display = `<ul class="selected_task_list">
        
        <li><b>Id Processo</b>: ${task_obj.ID_Proc}</li>
        <li><b>Processo</b>: ${task_obj.Proc}</li>
        <li><b>Task</b>: ${task_obj.Task}</li>
        <li><b>Role</b>: ${task_obj.Role}</li>
        <li><b>Doc</b>: ${task_obj.Doc}</li>
        <li><b>Imp/</b>: ${task_obj.Imp}</li>
        <li><b>Um</b>: ${task_obj.Um}</li>
        <li><b>Dt</b>: ${task_obj.Dt}</li>
        </ul>
        `
        open_task.innerHTML = task_to_display
    }
    else {

        let task_to_display = `<ul class="selected_task_list">
        
        <li><b>Id Processo</b>: ${task_obj.ID_Proc}</li>
        <li><b>Processo</b>: ${task_obj.Proc}</li>
        <li><b>Task</b>: ${task_obj.Task}</li>
        <li><b>Role</b>: ${task_obj.Role}</li>
        <li><b>Doc</b>: ${task_obj.Doc}</li>
        <li><b>To do</b>: ${task_obj.To_do}</li>
        <li><b>Imp/</b>: ${task_obj.Imp}</li>
        <li><b>Um</b>: ${task_obj.Um}</li>
        <li><b>Dt</b>: ${task_obj.Dt}</li>
        </ul>
        `
        open_task.innerHTML = task_to_display
    }
}

close_dialog_icon.addEventListener('click', close_dialog)
confirm_btn.addEventListener('click', on_confirm)
decline_btn.addEventListener('click', on_decline)

function load_data_to_obj(flag) {
    data_to_send.ID_Proc = task_obj.ID_Proc
    data_to_send.Task = task_obj.Task
    data_to_send.Flag = flag
}

function load_input_values() {
    let data_to_send_json = JSON.stringify(data_to_send)
    data_input[1].value = data_to_send_json
    console.log(`sending the obj: ${data_input[1].value}`)
}

function close_dialog() {
    task_dialog.close()
}

document.onkeydown = function key_press(e) {
    if(e.key ==="Escape") {
        close_dialog()
    }
}

function on_confirm() {
    let flag = true 
    load_data_to_obj(flag)
    load_input_values()
    /* console.log(`
    Retrieving data to send:\n
    Flag: ${flag},\n
    Process ID: ${task_obj.ID_Proc}\n
    Task: ${task_obj.Task}
    User: ${data_to_send.User_wf}
    `) */
}



function on_decline() {
    let flag = false
    load_data_to_obj(flag)
    load_input_values()
    /* console.log(`
    Retrieving data to send:\n
    Flag: ${flag},\n
    Process ID: ${task_obj.ID_Proc}\n
    Task: ${task_obj.Task}
    `) */
}

//MOBILE VIEW: processo[1], doc[4], to do[5](riga di sotto) ,imp[6]
function hide_table_content(element) {
    element.classList.add("hide_element")
}

export function show_elements(array) {
    for (let i in array) array[i].classList.remove("hide_element")
}

function select_elements_to_hide(array) {
    //take away things you don't want to hide
    array.splice(1, 1) // proc
    array.splice(3,1)//doc
    array.splice(4,1)//imp
}

function add_to_element_array(array) {
    for (let i in array) show_elements_array.push(array[i])
}

const columns = document.querySelectorAll(".th")
const cells = document.querySelectorAll(".cell")
var mobile = false //This flag is for the To do inside the processo.
if (window.innerWidth < 768) mobile_view()

function mobile_view() {
    let width = window.innerWidth;
    //if screen size is less than 768px (mobile), show mobile layout
    let id_proc_cell = document.querySelectorAll(".proc")
    let doc_cell = document.querySelectorAll(".doc")
    let imp_cell = document.querySelectorAll(".imp")
    let to_do_cell = document.querySelectorAll(".to_do")
    if(width < 768) {


        //convert node-list to array so you can .splice()
        let id_proc_array = [...id_proc_cell]
        let doc_array = [...doc_cell]
        let to_do_array = [...to_do_cell]
        let imp_array = [...imp_cell]
        let cells_array = [...cells]
        let column_array = [...columns]

        for(let i in to_do_array) { //MOVING THE TODO INSIDE THE PROCESSO
            if(mobile == false) {
                id_proc_array[i].innerHTML += `<div class="to_do_moved"><b>To do</b>: ${to_do_array[i].innerHTML}</div>`
            }
        }
        mobile = true

        //show_element_array contains all of the elements to show
        add_to_element_array(id_proc_array)
        add_to_element_array(doc_array)
        add_to_element_array(imp_array)
        // add_to_element_array(to_do_array)

        select_elements_to_hide(column_array)
        for (let i in column_array) hide_table_content(column_array[i])
        for(let i in cells_array) hide_table_content(cells_array[i])

        //after hiding all elements, show the ones you need
        show_elements(show_elements_array)
        
    } else {
        let cells_array = [...cells]
        let column_array = [...columns]
        let to_do_array = [...to_do_cell]
        let id_proc_array = [...id_proc_cell]
        show_elements(cells_array)
        show_elements(column_array)
        for(let i in to_do_array) { //MOVING THE TODO INSIDE THE PROCESSO
            console.log("going back to desktop view")
            let delete_text = id_proc_array[i].innerHTML
            delete_text = delete_text.replace(`<div class="to_do_moved"><b>To do</b>: ${to_do_array[i].innerHTML}</div>`, "")
            id_proc_array[i].innerHTML = delete_text
        }
        mobile = false
        
    }
}

window.addEventListener('resize', mobile_view)

console.log("end script")