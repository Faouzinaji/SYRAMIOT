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

		fetch('/finance/search_payment_entry',
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
                                
                                
                                
                                
                                <td>${item.student_id_id}</td>
                                <td>${item.semister_id}</td>
                                <td>${item.deposit_recipt}</td>
                                <td>${item.payment_date}</td>
                                <td>${item.payment_mode}</td>
                                <td>${item.recipt_voicher_no}</td>
                                <td>${item.amount_paid}</td>
                                <td>${item.discount}</td>
                                <td>${item.refund}</td>
                                <td>${item.add}</td>
                                <td>${item.drop}</td>
                                <td>${item.remarks}</td>
                                
                                
                                
                                


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