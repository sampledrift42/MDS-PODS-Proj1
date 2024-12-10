import pm4py
import pandas as pd

log = pm4py.read_xes(".//BPI_Challenge_2019.xes")

filtered_logs = {}
for item_category in log["case:Item Category"].unique():
    category_log = log[log["case:Item Category"] == item_category]
    for document_type in category_log["case:Document Type"].unique():
        category_df_by_document = category_log[
            category_log["case:Document Type"] == document_type
        ]
        filtered_logs[item_category + "_" + document_type] = category_df_by_document

allowed_start_act = {
    "3-way match, invoice before GR_EC Purchase order": [
        "SRM: Created",  # 796,
        "Vendor creates invoice",  #: 29,
        "Vendor creates debit memo",  #: 4,
    ],
    "3-way match, invoice before GR_Standard PO": [
        "Create Purchase Order Item",  #: 174844,
        "Vendor creates invoice",  #: 2634,
        "Create Purchase Requisition Item",  #: 42507,
        "Change Approval for Purchase Order",  #: 64,
        "Vendor creates debit memo",  #: 107,
        "Change Currency",  #: 2,
        "Release Purchase Order",  #: 22,
    ],
    "3-way match, invoice before GR_Framework order": [
        "Create Purchase Order Item"
    ],  # 1
    "3-way match, invoice after GR_EC Purchase order": [
        "SRM: Created",  #: 564,
        "Vendor creates invoice",  #: 44,
        "Vendor creates debit memo",  #: 2,
        "Create Purchase Order Item",  #: 1,
    ],
    "3-way match, invoice after GR_Standard PO": [
        "Create Purchase Order Item",  #: 12615,
        "Create Purchase Requisition Item",  #: 1219,
        "Vendor creates invoice",  #: 242,
        "Vendor creates debit memo",  #: 1,
    ],
    "3-way match, invoice after GR_Framework order": [
        "Vendor creates invoice",  #: 70,
        "Create Purchase Order Item",  #: 419,
        "Vendor creates debit memo",  #: 5,
    ],
    "Consignment_Standard PO": [
        "Create Purchase Order Item",  #: 11698,
        "Create Purchase Requisition Item",  #: 2800
    ],
    "2-way match_Framework order": [
        "Vendor creates invoice",  #: 438,
        "Change Approval for Purchase Order",  #: 314,
        "Vendor creates debit memo",  #: 3,
        "Create Purchase Order Item",  #: 289,
    ],
}

allowed_end_act = {
    "3-way match, invoice before GR_EC Purchase order": [
        "Clear Invoice",  #: 713,
        # "SRM: Transaction Completed",  #: 1,
        # "Record Invoice Receipt",  #: 45,
        # "Record Goods Receipt",  #: 39,
        # "Delete Purchase Order Item",  #: 4,
        # "SRM: In Transfer to Execution Syst.",  #: 4,
        # "Create Purchase Order Item",  #: 4,
        # "Cancel Invoice Receipt",  #: 3,
        # "Change Final Invoice Indicator",  #: 2,
        # "Remove Payment Block",  #: 5,
        # "SRM: Change was Transmitted",  #: 9,
    ],
    "3-way match, invoice before GR_Standard PO": [
        "Clear Invoice",  #: 171191,
        # "Record Invoice Receipt",  #: 21413,
        "Delete Purchase Order Item",  #: 7409,
        # "Cancel Invoice Receipt",  #: 1261,
        # "Change Quantity",  #: 406,
        # "Change Price",  #: 443,
        # "Record Goods Receipt",  #: 7288,
        # "Change Delivery Indicator",  #: 415,
        # "Block Purchase Order Item",  #: 167,
        # "Create Purchase Order Item",  #: 3714,
        # "Cancel Goods Receipt",  #: 209,
        # "Change Approval for Purchase Order",  #: 797,
        # "Remove Payment Block",  #: 5136,
        # "Change Currency",  #: 1,
        # "Reactivate Purchase Order Item",  #: 11,
        # "Cancel Subsequent Invoice",  #: 21,
        # "Change Storage Location",  #: 19,
        # "Vendor creates debit memo",  #: 2,
        # "Record Subsequent Invoice",  #: 9,
        # "Vendor creates invoice",  #: 49,
        # "Receive Order Confirmation",  #: 215,
        # "Release Purchase Order",  #: 1,
        # "Change payment term",  #: 1,
        # "Update Order Confirmation",  #: 2,
    ],
    "3-way match, invoice before GR_Framework order": [
        "Delete Purchase Order Item",  #: 1
    ],
    "3-way match, invoice after GR_EC Purchase order": [
        # "SRM: Transfer Failed (E.Sys.)",  #: 44,
        # "SRM: Change was Transmitted",  #: 38,
        # "Change Delivery Indicator",  #: 14,
        "Clear Invoice",  #: 347,
        # "SRM: In Transfer to Execution Syst.",  #: 26,
        # "Record Service Entry Sheet",  #: 12,
        # "Create Purchase Order Item",  #: 28,
        # "Record Invoice Receipt",  #: 67,
        # "Vendor creates debit memo",  #: 1,
        # "Change Final Invoice Indicator",  #: 1,
        # "SRM: Transaction Completed",  #: 5,
        # "Remove Payment Block",  #: 4,
        # "Cancel Invoice Receipt",  #: 4,
        # "Cancel Goods Receipt",  #: 1,
        # "Delete Purchase Order Item",  #: 4,
        # "Change Price",  #: 2,
        # "SRM: Deleted",  #: 9,
        # "Record Goods Receipt",  #: 4,
    ],
    "3-way match, invoice after GR_Standard PO": [
        "Clear Invoice",  #: 8674,
        # "Record Invoice Receipt",  #: 1171,
        # "Set Payment Block",  #: 58,
        # "Record Goods Receipt",  #: 2306,
        # "Record Service Entry Sheet",  #: 883,
        # "Cancel Invoice Receipt",  #: 77,
        "Delete Purchase Order Item",  #: 261,
        # "Cancel Goods Receipt",  #: 165,
        # "Remove Payment Block",  #: 252,
        # "Change Delivery Indicator",  #: 19,
        # "Create Purchase Order Item",  #: 154,
        # "Change Price",  #: 26,
        # "Vendor creates invoice",  #: 3,
        # "Change Quantity",  #: 20,
        # "Change Approval for Purchase Order",  #: 6,
        # "Cancel Subsequent Invoice",  #: 2,
    ],
    "3-way match, invoice after GR_Framework order": [
        # "Cancel Invoice Receipt",  #: 3,
        # "Change Price",  #: 46,
        "Clear Invoice",  #: 237,
        # "Delete Purchase Order Item",  #: 37,
        # "Record Invoice Receipt",  #: 92,
        # "Create Purchase Order Item",  #: 38,
        # "Record Service Entry Sheet",  #: 26,
        # "Record Goods Receipt",  #: 9,
        # "Cancel Goods Receipt",  #: 2,
        # "Cancel Subsequent Invoice",  #: 1,
        # "Vendor creates invoice",  #: 2,
        # "Reactivate Purchase Order Item",  #: 1,
    ],
    "Consignment_Standard PO": [
        # "Change Quantity",  #: 99,
        "Record Goods Receipt",  #: 13130,
        "Delete Purchase Order Item",  #: 404,
        # "Change Delivery Indicator",  #: 270,
        # "Receive Order Confirmation",  #: 17,
        # "Reactivate Purchase Order Item",  #: 2,
        # "Cancel Goods Receipt",  #: 63,
        # "Change Price",  #: 12,
        # "Update Order Confirmation",  #: 1,
        # "Change Storage Location",  #: 1,
        # "Create Purchase Order Item",  #: 499,
    ],
    "2-way match_Framework order": [
        "Change Approval for Purchase Order",  #: 543,
        "Clear Invoice",  #: 166,
        # "Record Invoice Receipt",  #: 303,
        # "Vendor creates debit memo",  #: 2,
        # "Vendor creates invoice",  #: 14,
        # "Delete Purchase Order Item",  #: 3,
        # "Set Payment Block",  #: 3,
        # "Create Purchase Order Item",  #: 10,
    ],
}

overall_rows = 0
for name, filtered_log in filtered_logs.items():
    print(name)
    print(len(filtered_log))
    overall_rows += len(filtered_log)
    print("startactivities")
    print(pm4py.get_start_activities(filtered_log))
    print("endactivities")
    print(pm4py.get_end_activities(filtered_log))
    # filtered_log = pm4py.filtering.filter_start_activities(filtered_log, [])
    filtered_log = pm4py.filtering.filter_end_activities(
        filtered_log, [allowed_end_act[name]]
    )
    filtered_log.to_csv(f"{name}.csv", index=False)
    # pm4py.write_xes(filtered_log, f"{name}.xes")


print(overall_rows)
print(len(log))
