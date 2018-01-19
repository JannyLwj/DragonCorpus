var TableEditable_Intent = function () {

    return {

        //main function to initiate the module
        init: function () {
            function restoreRow(oTable_intent, nRow) {
                var aData = oTable_intent.fnGetData(nRow);
                var jqTds = $('>td', nRow);

                for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                    oTable_intent.fnUpdate(aData[i], nRow, i, false);
                }

                oTable_intent.fnDraw();
            }

            function editRow(oTable_intent, nRow) {
                var aData = oTable_intent.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                jqTds[1].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[1] + '">';
                jqTds[2].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[2] + '">';
                jqTds[3].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[3] + '">';
                jqTds[4].innerHTML = '<a class="edit" href="">Save</a>';
                jqTds[5].innerHTML = '<a class="cancel" href="">Cancel</a>';
            }

            function saveRow(oTable_intent, nRow) {
                var jqInputs = $('input', nRow);
                oTable_intent.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable_intent.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable_intent.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable_intent.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 4, false);
                oTable_intent.fnUpdate('<a class="delete" href="">Delete</a>', nRow, 5, false);
                oTable_intent.fnDraw();
            }

            function cancelEditRow(oTable_intent, nRow) {
                var jqInputs = $('input', nRow);
                oTable_intent.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable_intent.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable_intent.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable_intent.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 4, false);
                oTable_intent.fnDraw();
            }

            var oTable_intent = $('#sample_editable_intent').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                "iDisplayLength": 20,
                "sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
            });

            jQuery('#sample_editable_intent .group-checkable').change(function () {
                var set = jQuery(this).attr("data-set");
                var checked = jQuery(this).is(":checked");
                jQuery(set).each(function () {
                    if (checked) {
                        $(this).attr("checked", true);
                    } else {
                        $(this).attr("checked", false);
                    }
                });
                jQuery.uniform.update(set);
            });

            jQuery('#sample_editable_intent_wrapper .dataTables_filter input').addClass("m-wrap medium"); // modify table search input
            jQuery('#sample_editable_intent_wrapper .dataTables_length select').addClass("m-wrap small"); // modify table per page dropdown
            jQuery('#sample_editable_intent_wrapper .dataTables_length select').select2({
                showSearchInput : false //hide search box with special css class
            }); // initialzie select2 dropdown

            var nEditing = null;

            $('#sample_editable_intent_new').click(function (e) {
                e.preventDefault();
                var aiNew = oTable_intent.fnAddData(['<div class="checker"><span><td><input type="checkbox" class="checkboxes" value="1" /></td></span></div>', '', '', '',
                        '<a class="edit" href="">Edit</a>', '<a class="cancel" data-mode="new" href="">Cancel</a>'
                ]);
                var nRow = oTable_intent.fnGetNodes(aiNew[0]);
                editRow(oTable_intent, nRow);
                nEditing = nRow;
            });

            $('#sample_editable_intent a.delete').live('click', function (e) {
                e.preventDefault();

                if (confirm("Are you sure to delete this row ?") == false) {
                    return;
                }

                var nRow = $(this).parents('tr')[0];
                oTable_intent.fnDeleteRow(nRow);
                alert("Deleted! Do not forget to do some ajax to sync with backend :)");
            });

            $('#sample_editable_intent a.cancel').live('click', function (e) {
                e.preventDefault();
                if ($(this).attr("data-mode") == "new") {
                    var nRow = $(this).parents('tr')[0];
                    oTable_intent.fnDeleteRow(nRow);
                } else {
                    restoreRow(oTable_intent, nEditing);
                    nEditing = null;
                }
            });

            $('#sample_editable_intent a.edit').live('click', function (e) {
                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable_intent, nEditing);
                    editRow(oTable_intent, nRow);
                    nEditing = nRow;
                } else if (nEditing == nRow && this.innerHTML == "Save") {
                    /* Editing this row and want to save it */
                    saveRow(oTable_intent, nEditing);
                    nEditing = null;
                    alert("Updated! Do not forget to do some ajax to sync with backend :)");
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable_intent, nRow);
                    nEditing = nRow;
                }
            });
        }

    };

}();