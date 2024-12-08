def align_center(x):
    return ["text-align: left" for x in x]


def getTitleFormat(workbook):
    return workbook.add_format({
            "bold": True,
            "border": 2,
            "align": "center",
            "valign": "vcenter",
            "font_size": 17,            
        }
    )


def getHeaderBoldCenter(workbook):
    return workbook.add_format({
            "bold": True,
            "align": 'center',
            "valign": 'vcenter',
            "font_size": 12,
            "border": 1,
        }
    )
    
def headerNonBold(workbook):
    return workbook.add_format({
            "align": 'center',
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
        }
    )

def getHeaderFormat(workbook):
    return workbook.add_format({
            "bold": True,
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
        }
    )

def getNormalFormat(workbook):
    return workbook.add_format({
            "font_size": 12,
        }
    )

def getWarningFormat(workbook):
    return workbook.add_format({
            "font_color": 'red',
            "font_size": 12
        }
    )
def getWarningBoldFormat(workbook):
    return workbook.add_format({
            "font_color": 'red',
            "bold": True,
            "font_size": 12
        }
    )

def getHeaderWarningFormat(workbook):
    return workbook.add_format({
            "bold": True,
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            "font_color": 'red',
        }
    )

def getNormalBoldFormat(workbook):
    return workbook.add_format({
            "bold": True,
            "font_size": 12,
        }
    )

# def getTitleFormat(workbook):
#     return workbook.add_format(
#         {
#             "bold": True,
#             "border": 2,
#             # "fg_color": "#051094",
#             "font_size": 17,
#             # "font_color": "white",
#             # "border_color": "white",
#             
#         }
#     )