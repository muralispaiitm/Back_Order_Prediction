

class GlobalVariablesPath:
    def __init__(self):
        self.filesPath = {"dataSet"         : "Files_Storage/DataSet/",
                          "trainingFile"    : "Files_Storage/DataSet/Training/Training_BOP.csv",
                          "testingFile"     : "Files_Storage/DataSet/Testing/Testing_BOP.csv",
                          "predictingFiles" : "Files_Storage/DataSet/Predicting/",
                          "PickleFiles"     : "Files_Storage/PickleFiles/",
                          "Figures"         : "Files_Storage/Figures/",
                          "Temp"            : "Files_Storage/Temp/"
                          }
        self.syntaxErrorVal = -99
        self.CategoricalFeatures = ["potential_issue", "deck_risk", "oe_constraint", "ppap_risk", "stop_auto_buy", "rev_stop", "went_on_backorder"]
        self.NumericalFeatures = ["national_inv", "lead_time", "in_transit_qty", "forecast_3_month", "forecast_6_month", "forecast_9_month",
                                  "sales_1_month", "sales_3_month", "sales_6_month", "sales_9_month", "min_bank", "pieces_past_due",
                                  "perf_6_month_avg", "perf_12_month_avg", "local_bo_qty"]
        self.SelectedFeatures_for_backorder = ["national_inv", "lead_time", "in_transit_qty", "forecast_9_month", "sales_9_month", "perf_6_month_avg",  "min_bank", "pieces_past_due", "local_bo_qty",
                                               "deck_risk", "ppap_risk", "stop_auto_buy", "went_on_backorder"
                                               ]
        self.SelectedFeatures_for_minbank = ["national_inv", "lead_time", "in_transit_qty", "forecast_6_month", 'sales_3_month', "perf_6_month_avg", "min_bank", 'pieces_past_due', 'local_bo_qty',
                                             'deck_risk', 'ppap_risk', 'stop_auto_buy', 'oe_constraint', 'potential_issue', 'rev_stop']

        self.MySQL_Variables = {"host"          : "localhost",
                                "user"          : "root",
                                "pwd"           : "password",
                                "database"      : "backorderproduct",
                                "trainingTable" : "training_BOP",
                                "testingTable"  : "testing_BOP"
                                }

        self.ValuesOfCategorical = ["No", "Yes"]
        self.ColNames = ["sku", "potential_issue", "deck_risk", "oe_constraint", "ppap_risk", "stop_auto_buy",
                         "rev_stop",
                         "went_on_backorder", "national_inv", "lead_time", "in_transit_qty", "forecast_3_month",
                         "forecast_6_month",
                         "forecast_9_month", "sales_1_month", "sales_3_month", "sales_6_month", "sales_9_month",
                         "min_bank", "pieces_past_due",
                         "perf_6_month_avg", "perf_12d_month_avg", "local_bo_qty"
                         ]
