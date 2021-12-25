# sort_nested_dict_by_value
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

import tkinter as tk

# for Python 3.7+

progeny_dicts = {
    6: {"sorter": (4,9,6), "partner_id": None, "partner_name": "", "parent_type": "",
        "partner_kin_type": "", "findings_persons_id": None, "children": [{"name": "Jack"}, {}, {}],
        "marital_events": {"findings_persons_id": None, "date": "-0000-00-00-------",
        "finding": None}
}, 
    5599: {"sorter": (2,19,16), "partner_id": None, "partner_name": "", 
        "parent_type": "", "partner_kin_type": "", "findings_persons_id": None, 
        "children": [{"name": "Jill"}, {}, {}], 
        "marital_events": {"findings_persons_id": None, "date": "-0000-00-00-------", 
        "finding": None}
}, 
    5635: {"sorter": (2,9,16), "partner_id": None, "partner_name": "", 
        "parent_type": "", "partner_kin_type": "", "findings_persons_id": None, 
        "children": [{"name": "Jeff"}, {}, {}], 
        "marital_events": {"findings_persons_id": None, "date": "-0000-00-00-------", 
        "finding": None}
}
}

# what's being sorted is the k,v tuples, thus the [1] for v:
progeny_dicts = dict(sorted(progeny_dicts.items(), key=lambda i: i[1]["sorter"]))




root = tk.Tk()

x = 0
for k,v in progeny_dicts.items():
    lab = tk.Label(root, text=k)
    lab.grid(column=0, row=x)
    ent = tk.Entry(root)
    ent.grid(column=1, row=x)
    ent.insert(0, v["sorter"])
    ll = tk.Label(root, text=v["children"][0]["name"])
    ll.grid(column=2, row=x)
    x += 1


root.mainloop()

