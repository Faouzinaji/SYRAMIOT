const searchField = document.getElementById('searchField');
const table_output = document.getElementById('outputtable');
const app_table = document.getElementById('apptable');
const paginationcontainer=document.getElementById('paginationcontainer');
const tbody=document.getElementById('outputtablebody');
table_output.style.display='none';




searchField.addEventListener('keyup', (e) => {

	const searchvalue=e.target.value;

	if (searchvalue.trim().length>0)
	{
        tbody.innerHTML='';
        paginationcontainer.style.display='none';

		fetch('/registrar/search_student',
			{
				method:"POST",



			body:JSON.stringify({searchText:searchvalue}),

		})

			.then((res) => res.json())
			.then((data)=>
			{
			    console.log('data',data);
                app_table.style.display='none';
                table_output.style.display='block';

                if(data.length===0)
                {
                    table_output.innerHTML='No record found';

                }
                else
                    {

                    data.forEach((item) =>
                        {
                        tbody.innerHTML+=
                            `<tr>
                                <td>${item.student_id}</td>
                                
                                <td>${item.first_name}</td>
                                
                                <td>${item.second_name}</td>
                                <td>${item.last_name}</td>
                                <td>${item.DOB}</td>
                                <td>${item.Sex}</td>
                                <td>${item.department}</td>
                                <td>${item.scholar}</td>
                                <td>${item.telephone}</td>
                                <td>${item.Email}</td>
                                <td>${item.buch}</td>
                                <td>${item.Senseion}</td>
                                <td>${item.section}</td>
                                <td>${item.crash}</td>
                                <td>${item.registered_by}</td>
                                <td>${item.Registered_on}</td>
                                


                            </tr>`;

                        });
                }

			});
	}
	else {
	    table_output.style.display='none';
	    app_table.style.display='block';
	    paginationcontainer.style.display='block';
    }


});