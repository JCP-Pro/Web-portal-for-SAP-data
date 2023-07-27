const user_wf = document.querySelector('.user_wf').textContent
const file_name = user_wf+'_tasks.json'
const root_url = './tasks/'
// const fs = require('fs')
// const complete_file_url = root_url+file_name
//Diaolog buttons
const task_dialog = document.querySelector(".task_dialog")
const close_dialog_icon = document.querySelector(".exit_dialog_container")
const confirm_btn = document.querySelector(".confirm_btn")
const decline_btn = document.querySelector(".decline_btn")
//Task_obj for sending data
const task_obj = {
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
}

const file_name_to_send = user_wf+'_data.json'
const send_url_root = "C:/Users/jpineda/Desktop/django_login_form/login_project/static/data/users/"
const destination_url = send_url_root+file_name

/* 
For testing in the console.
const task_data = []
 */
import('./tasks/'+file_name, { assert: { type: "json" } })
.then((json_task)=> {
    let array_of_task = json_task.default
    load_data_to_table(array_of_task)
})
.catch(err => console.log(`there has been an error: ${err}`))

let tbody = document.querySelector(".task_body")
let row, cell

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
        cell.textContent = data[i].ID_Proc
        cell = row.insertCell()
        cell.textContent = data[i].Proc
        cell = row.insertCell()
        cell.textContent = data[i].Task
        cell = row.insertCell()
        cell.textContent = data[i].Role
        cell = row.insertCell()
        cell.textContent = data[i].Doc
        cell = row.insertCell()
        cell.textContent = data[i].To_do
        cell = row.insertCell()
        cell.textContent = data[i].Imp.trim()
        cell = row.insertCell()
        cell.textContent = data[i].Um
        cell = row.insertCell()
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
            id_process = selected_row.cells[0].innerHTML
            process = selected_row.cells[1].innerHTML
            task = selected_row.cells[3].innerHTML
            role = selected_row.cells[4].innerHTML
            doc = selected_row.cells[5].innerHTML
            imp = selected_row.cells[6].innerHTML
            um = selected_row.cells[7].innerHTML
            dt = selected_row.cells[8].innerHTML

            task_obj.ID_Proc = id_process
            task_obj.Proc = process
            task_obj.Task = task
            task_obj.Role = role
            task_obj.Doc = doc
            task_obj.Imp = imp
            task_obj.Um = um
            task_obj.Dt = dt
            break
        }
    }

    task_obj_json = JSON.stringify(task_obj)

    show_dialog()
}

function show_dialog() {
    task_dialog.show()
    let open_task = document.querySelector(".current_task")
    let task_to_display = `<ul>
    
    <li><b>Id Processo</b>: ${task_obj.ID_Proc}</li>
    <li><b>Processo</b>: ${task_obj.Proc}</li>
    <li><b>Task</b>: ${task_obj.Task}</li>
    <li><b>Role</b>: ${task_obj.Role}</li>
    <li><b>Doc</b>: ${task_obj.Doc}</li>
    <li><b>To do</b>: ${task_obj.To_do}</li>
    <li><b>Imp/<b>: ${task_obj.Imp}</li>
    <li><b>Um</b>: ${task_obj.Um}</li>
    <li><b>Dt</b>: ${task_obj.Dt}</li>
    </ul>
    `
    open_task.innerHTML = task_to_display
}

close_dialog_icon.addEventListener('click', close_dialog)
confirm_btn.addEventListener('click', on_confirm)
decline_btn.addEventListener('click', on_decline)

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
    console.log(`
    Retrieving data to send:\n
    Flag: ${flag},\n
    Process ID: ${task_obj.ID_Proc}\n
    Task: ${task_obj.Task}
    `)
    data_to_send.ID_Proc = task_obj.ID_Proc
    data_to_send.Task = task_obj.Task
    data_to_send.Flag = flag
    
    save_data_to_file(data_to_send)
}

function on_decline() {
    let flag = false
    data_to_send.ID_Proc = task_obj.ID_Proc
    data_to_send.Task = task_obj.Task
    data_to_send.Flag = flag

    console.log(`
    Retrieving data to send:\n
    Flag: ${flag},\n
    Process ID: ${task_obj.ID_Proc}\n
    Task: ${task_obj.Task}
    `)

    save_data_to_file(data_to_send)
}

function save_data_to_file(js_obj) {
    let json_data = JSON.stringify(js_obj)
    console.log(`This is the data i will send: ${json_data}`)

   //TODO: Save the json_data to a json file to be retrieved in python. From python send the json data to the webservice.
   
   /* fs.writeFile(file_name_to_send, json_data, (err) => {
    if (err){
        console.log(err)
    }
   }) */

   /* 
    TODO: Look at browsify to use "require()" https://browserify.org/
    then look at https://github.com/browserify/browserify#usage
    You will find -o 
    this command should have C:\Users\jpineda\Desktop\django_login_form\login_project\static\scripts\users\bundle\bundle.js as file destination.
   */
}