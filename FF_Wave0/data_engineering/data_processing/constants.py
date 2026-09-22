class ANAPLAN_API_PROCESS:
    LOGS = "snacking_eus2_{ENV}.mw_finance_mwd30anaplan.anaplan_api_logs"
    MARS_CALENDAR = "mars_cal"

    class ACTUALS:
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        # Original Model and file id
        MODEL_ID = "05D2BC163D0A48A78D6CAE6BB89BF7AC"
        FILE_ID = "113000000194"
        PROCESS_ID = "118000000032"
        INPUT_DF = "actual_ep_sansep"
        # Test Model and Test File
        # MODEL_ID = "B801525CEA254A90B32ADBBD727F4C82"
        # FILE_ID = "113000000185"

    class ACTUALS_NEW:
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000475"
        PROCESS_ID = "118000000080"
        INPUT_DF = "df_actuals"

    class HEADCOUNT:
        INPUT_DF = "headcount_output"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "05D2BC163D0A48A78D6CAE6BB89BF7AC"
        FILE_ID = "113000000195"
        PROCESS_ID = "118000000033"

    class PRODUCT_MASTERDATA:
        INPUT_DF = "product_masterdata_anaplan"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000446"
        PROCESS_ID = "118000000049"

    class CUSTOMER_MASTERDATA:
        INPUT_DF = "customer_masterdata_anaplan"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000415"
        PROCESS_ID = "118000000074"

    class TPM:
        INPUT_DF = "df_trade_promo"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000485"
        PROCESS_ID = "118000000084"

    class CUSTOMER_PRICE_LIST:
        INPUT_DF = "df_customer_price_list"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000457"
        PROCESS_ID = "118000000081"

    class STANDARD_COST:
        INPUT_DF = "df_standard_cost"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000450"
        PROCESS_ID = "118000000078"

    class ICP:
        INPUT_DF = "df_icp"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000452"
        PROCESS_ID = "118000000079"

    class SUPPLY:
        INPUT_DF = "df_supply"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000460"
        PROCESS_ID = "118000000082"

    class DEMAND:
        INPUT_DF = "df_demand"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "CC22140982BA44249C8FB49201347B58"
        FILE_ID = "113000000461"
        PROCESS_ID = "118000000083"


class ANAPLAN_DATA_PROCESSING:
    SANS_EP_INPUT = "sans_ep"
    HEADCOUNT_INPUT = "headcount"
    HEADCOUNT_OUTPUT = "headcount_output"
    EP_INPUT = "ep"
    PC_MAPPING = "pc_mapping"
    UNIT_MAPPING = "unit_mapping"
    ACTUAL_OUTPUT = "actual_ep_sansep"
    ACTUALS_COLUMN_ORDER = [
        "Transaction_ID",
        "Submission_Type_ID",
        "Submission_Type",
        "Fiscal_Year_Period",
        "date_ids",
        "Unit_ID",
        "Unit_Description",
        "Destination_Unit_ID",
        "Destination_Unit_Description",
        "RL_ID",
        "RL_Description",
        "Brand_Flag_ID",
        "Brand_Flag",
        "EC_Group_ID",
        "EC_Group",
        "Product_Segment_ID",
        "Product_Segment",
        "Product_Sub_Segment_ID",
        "Product_Sub_Segment",
        "Value_CY",
        "Value_LY",
    ]
    HEADCOUNT_COLUMN_ORDER = [
        "Transaction_ID",
        "Date_ID",
        "date_ids",
        "Unit_ID",
        "Unit_Description",
        "RL_ID",
        "RL_Description",
        "Value",
    ]


class RETROFIT_PROCESS_DATA:
    DIMENSION_ENTITY = "dimension_entity"
    DIMENSION_ACCOUNT = "dimensions_account"
    DIMENSION_CURRENCY = "dimensions_currency"
    DIMENSION_ITEM_TAXONOMY = "dimensions_item_taxonomy"
    DIMENSION_IT_EC_GROUP = "dimensions_it_ec_group"
    DIMENSION_IT_BRAND_FLAG = "dimensions_it_brand_flag"
    DIMENSION_VW_ITEM_PRODUCT_CATEGORY = "dimensions_vw_item_product_category"
    DIMENSION_ACCOUNT_CATEGORY = "dimensions_account_category"
    DIMENSION_ENTITY_HIERARCHY = "dimensions_entity_hierarchy"
    FACT_FINANCIALS_CONSOLIDATED = (
        "daas_vw_facts_financial_consolidated_rls_account_entity"
    )
    FACT_FINANCIALS_EP = "daas_vw_facts_financial_rls_ep_account_entity"
    UNIT_MAPPING = "unit_mapping"
    UNOFFICIAL_MAPPING = "unofficial_mapping"
    EP_OUTPUT = "ep_output"
    ACTUALS_OUTPUT = "actuals_output"
    PRODUCT_MASTER = "products_master"
    HEADCOUNT_OUTPUT = "headcount_output"
    ACCOUNTS_MASTER = "accounts_master"
    ENTITY_HIERARCHY = "entity_hierarchy"
    PC_MAPPING = "pc_mapping"
    RL_ID_FILTERS = "rl_id_filter"
    HEADCOUNT_COLUMN_ORDER = [
        "Transaction_ID",
        "Date_ID",
        "date_ids",
        "Entity_ID",
        "Entity_Description",
        "Account_ID",
        "Account_Description",
        "Value",
    ]
    SANSEP_API_FIT_COLUMN_ORDER = [
        "Transaction_ID",
        "Submission_Type_ID",
        "Submission_Type",
        "Fiscal_Year_Period",
        "date_ids",
        "Unit_ID",
        "Unit_Description",
        "Destination_Unit_ID",
        "Destination_Unit_Description",
        "RL_ID",
        "RL_Description",
        "Brand_Flag_ID",
        "Brand_Flag",
        "EC_Group_ID",
        "EC_Group",
        "Product_Segment_ID",
        "Product_Segment",
        "Product_Sub_Segment_ID",
        "Product_Sub_Segment",
        "Value_CY",
        "Value_LY",
    ]
    SANSEP_COLUMN_ORDER = [
        "Transaction_ID",
        "Submission_Type_ID",
        "Submission_Type",
        "Fiscal_Year_Period",
        "date_ids",
        "Entity_ID",
        "Entity_Description",
        "Destination_Entity_ID",
        "Destination_Entity_Description",
        "Account_ID",
        "Account_Description",
        "Brand_Flag_ID",
        "Brand_Flag",
        "EC_Group_ID",
        "EC_Group",
        "Product_Segment_ID",
        "Product_Segment",
        "Product_Sub_Segment_ID",
        "Product_Sub_Segment",
        "Value_CY",
        "Value_LY",
    ]
    PRODUCT_MASTER_COLS = [
        "Brand_Flag_ID",
        "Brand_Flag",
        "EC_Group_ID",
        "EC_Group",
        "Product_Segment_ID",
        "Product_Segment",
        "Product_Sub_Segment_ID",
        "Product_Sub_Segment"
    ]

    class ACCOUNT_MASTER_DATA:
        RENAME_COLS_DICT = {
            "Account_ID": "Account_ID",
            "Account_Alias": "Account_Description",
            "Account_Category_Alias": "Account_Category",
        }

    class ENTITY_HIERARCHY_DATA:
        ordered_cols = [
            "S_NO",
            "Parent_Entity_ID",
            "Entity_ID",
            "Entity_Alias",
            "Level3_Entity_ID",
            "Level4_Entity_ID",
            "Level5_Entity_ID",
            "Level6_Entity_ID",
            "Level7_Entity_ID",
            "Level8_Entity_ID",
            "Level9_Entity_ID",
            "Level10_Entity_ID",
            "Level11_Entity_ID",
            "Level12_Entity_ID",
            "Level13_Entity_ID",
            "Level14_Entity_ID",
            "Level15_Entity_ID",
            "Type",
        ]
        RENAME_COLS_DICT = {
            "S_NO": "S_NO",
            "Parent_Entity_ID": "PARENT_CODE",
            "Entity_ID": "CODE",
            "Entity_Alias": "DESCR",
            "Level3_Entity_ID": "GEN1",
            "Level4_Entity_ID": "GEN2",
            "Level5_Entity_ID": "GEN3",
            "Level6_Entity_ID": "GEN4",
            "Level7_Entity_ID": "GEN5",
            "Level8_Entity_ID": "GEN6",
            "Level9_Entity_ID": "GEN7",
            "Level10_Entity_ID": "GEN8",
            "Level11_Entity_ID": "GEN9",
            "Level12_Entity_ID": "GEN10",
            "Level13_Entity_ID": "GEN11",
            "Level14_Entity_ID": "GEN12",
            "Level15_Entity_ID": "GEN13",
            "Type": "TYPE",
        }


class MASTERDATA_PROCESSING:
    class CUSTOMER_MASTERDATA:
        CUSTOMER_MASTERDATA_OUTPUT = "df_customer_masterdata"
        CUSTOMER_MASTERDATA_ANAPLAN = "customer_masterdata_anaplan"

        CUSTOMER_MASTERDATA_QUERY = """

            WITH customer_base AS (
        SELECT DISTINCT KUNNR_PK AS Customer, LOEVM AS Marked_for_Deletion
        FROM `0CUSTOMER_ATTR`
    ),
    all_text AS (
        SELECT DISTINCT KUNNR_PK, TXTMD AS Name
        FROM `0CUSTOMER_TEXT`
    ),
    sales AS (
        SELECT DISTINCT
            KUNNR_PK AS Customer,
            VKORG_PK AS Sales_Org,
            VTWEG_PK AS Distribution_Channel,
            SPART_PK AS Division,
            PLTYP    AS Price_List
        FROM `0CUST_SALES_ATTR`
    ),
    sold_to AS (
        SELECT DISTINCT
            KUNNR_PK AS Customer,
            KUNN2_PK AS Sold_To,
            VKORG_PK AS Sales_Org,
            VTWEG_PK AS Distribution_Channel,
            SPART_PK AS Division
        FROM `ZCUSTOPF_ATTR`
        WHERE PARVW_PK = 'SP'
    ),
    payer AS (
        SELECT DISTINCT
            KUNNR_PK AS Customer,
            KUNN2_PK AS Payer,
            VKORG_PK AS Sales_Org,
            VTWEG_PK AS Distribution_Channel,
            SPART_PK AS Division
        FROM `ZCUSTOPF_ATTR`
        WHERE PARVW_PK = 'PY'
    ),
    ship_to AS (
        SELECT DISTINCT
            KUNNR_PK AS Customer,
            KUNN2_PK AS Ship_To,
            VKORG_PK AS Sales_Org,
            VTWEG_PK AS Distribution_Channel,
            SPART_PK AS Division
        FROM `ZCUSTOPF_ATTR`
        WHERE PARVW_PK = 'SH'
    ),
    demand_grp AS (
        SELECT DISTINCT
            KUNNR_PK AS Customer,
            KUNN2_PK AS Demand_Group,
            VKORG_PK AS Sales_Org,
            VTWEG_PK AS Distribution_Channel,
            SPART_PK AS Division
        FROM `ZCUSTOPF_ATTR`
        WHERE PARVW_PK = 'ZC'
    )
    SELECT DISTINCT
        concat_ws('_', coalesce(regexp_replace(c.Customer, '^0+', ''), '000'),
        coalesce(s.Sales_Org, '000'), coalesce(s.Distribution_Channel, '000'),
        coalesce(s.Division, '000')) AS `Code`,
        regexp_replace(c.Customer, '^0+', '')       AS `Customer`,
        cd.Name                                     AS `Customer Desc`,
        c.Marked_for_Deletion                       AS `Marked_For_Deletion`,
        s.Sales_Org                                 AS `Sales Org`,
        s.Distribution_Channel                      AS `Distribution Channel`,
        s.Division,
        regexp_replace(st.Sold_To, '^0+', '')       AS `Sold-To`,
        sd.Name                                     AS `Sold-To Desc`,
        regexp_replace(py.Payer, '^0+', '')         AS `Payer`,
        pd.Name                                     AS `Payer Desc`,
        regexp_replace(sh.Ship_To, '^0+', '')       AS `Ship-To`,
        shd.Name                                    AS `Ship-To Desc`,
        regexp_replace(dg.Demand_Group, '^0+', '')  AS `Demand Group`,
        dgd.Name                                    AS `Demand Group Desc`,
        s.Price_List                                AS `Price List`
    FROM customer_base c
    LEFT JOIN all_text   cd  ON c.Customer = cd.KUNNR_PK
    LEFT JOIN sales      s   ON c.Customer = s.Customer
    LEFT JOIN sold_to    st
        ON s.Customer             = st.Customer
    AND s.Sales_Org            = st.Sales_Org
    AND s.Distribution_Channel = st.Distribution_Channel
    AND s.Division             = st.Division
    LEFT JOIN payer      py
        ON s.Customer             = py.Customer
    AND s.Sales_Org            = py.Sales_Org
    AND s.Distribution_Channel = py.Distribution_Channel
    AND s.Division             = py.Division
    LEFT JOIN ship_to    sh
        ON s.Customer             = sh.Customer
    AND s.Sales_Org            = sh.Sales_Org
    AND s.Distribution_Channel = sh.Distribution_Channel
    AND s.Division             = sh.Division
    LEFT JOIN demand_grp dg
        ON s.Customer             = dg.Customer
    AND s.Sales_Org            = dg.Sales_Org
    AND s.Distribution_Channel = dg.Distribution_Channel
    AND s.Division             = dg.Division
    LEFT JOIN all_text sd  ON st.Sold_To      = sd.KUNNR_PK
    LEFT JOIN all_text pd  ON py.Payer        = pd.KUNNR_PK
    LEFT JOIN all_text shd ON sh.Ship_To      = shd.KUNNR_PK
    LEFT JOIN all_text dgd ON dg.Demand_Group = dgd.KUNNR_PK
    """

    class PRODUCT_MASTERDATA:
        PRODUCT_MASTERDATA_OUTPUT = "df_product_masterdata"
        PRODUCT_MASTERDATA_ANAPLAN = "product_masterdata_anaplan"
        PRODUCT_MASTERDATA_QUERY = """
            SELECT
        -- =====================================================
        -- CORE MATERIAL
        -- =====================================================
        regexp_replace(ma.MATNR_PK,'^0+','')                     AS `Material_SKU`,
        mt.TXTMD                                                 AS `Material_Desc`,
        ma.MTART                                                 AS `Material_Type`,
        ma.LVORM                                                 AS `Marked_For_Deletion`,
        -- =====================================================
        -- REPRESENTATIVE MATERIAL
        -- =====================================================
        regexp_replace(ma.ZZREPMATNR,'^0+','')                   AS `ZREP`,
        mt_rep.TXTMD                                             AS `ZREP_Desc`,

        -- =====================================================
        -- IDENTIFIERS
        -- =====================================================
        ma.EAN11                                                 AS `EAN`,
        ma.MEINS                                                 AS `Base_UOM`,

        -- =====================================================
        -- TRADED UNIT FORMAT
        -- =====================================================
        ma.ZZCLF20                                               AS `Traded_Unit_Format`,
        CONCAT(tuf.CHRVAL, '/', tuf.VTEXT)                       AS `Traded_Unit_Format_Desc`,

        -- =====================================================
        -- WEIGHT
        -- =====================================================
        ma.GEWEI                                                 AS `Weight_Unit`,
        CAST(ma.BRGEW AS DECIMAL(18,3))                          AS `Gross_Weight`,
        CAST(ma.NTGEW AS DECIMAL(18,3))                          AS `Net_Weight`,

        -- =====================================================
        -- BUSINESS / MARKET SEGMENT
        -- =====================================================
        ma.ZZCLF01                                               AS `Business_Segment_Id`,
        bs.VTEXT                                                 AS `Business_Segment_Desc`,
        ma.ZZCLF02                                               AS `Market_Segment`,

        -- =====================================================
        -- BRAND
        -- =====================================================
        ma.ZZCLF03                                               AS `Brand_Flag`,
        bf.VTEXT                                                 AS `Brand_Flag_Desc`,
        ma.ZZCLF04                                               AS `Brand_Sub_Flag`,
        CONCAT(bsf.CHRVAL, '/', bsf.VTEXT)                       AS `Brand_Sub_Flag_Desc`,

        -- =====================================================
        -- MULTIPACK / PACK / CONSUMER PACK
        -- =====================================================
        ma.ZZCLF10                                               AS `Multipack_Quantity`,
        CONCAT(mp.CHRVAL, '/', mp.VTEXT)                         AS `Multipack_Quantity_Desc`,
        ma.ZZCLF18                                               AS `Product_Pack_Size_Group`,
        ppsg.VTEXT                                               AS `Product_Pack_Size_Group_Desc`,
        ma.ZZCLF17                                               AS `Consumer_Pack_Type`,
        cpt.VTEXT                                                AS `Consumer_Pack_Type_Desc`,

        -- =====================================================
        -- PRODUCT ATTRIBUTES
        -- =====================================================
        dpps.IT_Product_Pack_Size_Alias                          AS `Product_Pack_Size`,
        dpc.IT_Product_Category_Alias                            AS `Product_Category`,
        ma.ZZCLF13                                               AS `Product_Type`,

        -- =====================================================
        -- TRADED UNIT CONFIGURATION
        -- =====================================================
        ma.ZZCLF21                                               AS `Traded_Unit_Configuration`,
        CONCAT(tuc.CHRVAL, '/', tuc.VTEXT)                       AS `Traded_Unit_Configuration_Desc`,

        -- =====================================================
        -- ENTERPRISE TAXONOMY
        -- =====================================================
        dt.IT_EC_Group_ID                                        AS `EC_Group`,
        ecg.IT_EC_Group_Alias                                    AS `EC_Group_Description`,
        vw.Product_Segment_ID                                    AS `Product_Segment`,
        vw.Product_Segment                                       AS `Product_Segment_Description`,
        vw.Product_Sub_Segment_ID                                AS `Product_Sub_Segment`,
        vw.Product_Sub_Segment                                   AS `Product_Sub_Segment_Description`

        FROM `0MATERIAL_ATTR` ma

        LEFT JOIN `0MATERIAL_TEXT` mt
            ON ma.MATNR_PK = mt.MATNR
            AND mt.SPRAS = 'EN'

        LEFT JOIN `0MATERIAL_TEXT` mt_rep
            ON ma.ZZREPMATNR = mt_rep.MATNR
            AND mt_rep.SPRAS = 'EN'

        LEFT JOIN `ZCLF01_TEXT` bs
            ON CAST(ma.ZZCLF01 AS STRING) = bs.CHRCOD_PK

        LEFT JOIN `ZBRAND_TEXT` bf
            ON CAST(ma.ZZCLF03 AS STRING) = bf.CHRCOD_PK

        LEFT JOIN `ZBRANDS_TEXT` bsf
            ON CAST(ma.ZZCLF04 AS STRING) = bsf.CHRCOD_PK

        LEFT JOIN `ZCLF10_TEXT` mp
            ON CAST(ma.ZZCLF10 AS STRING) = mp.CHRCOD

        LEFT JOIN `ZCLF17_TEXT` cpt
            ON CAST(ma.ZZCLF17 AS STRING) = cpt.CHRCOD_PK

        LEFT JOIN `ZCLF18_TEXT` ppsg
            ON CAST(ma.ZZCLF18 AS STRING) = ppsg.CHRCOD

        LEFT JOIN `ZCLF20_TEXT` tuf
            ON CAST(ma.ZZCLF20 AS STRING) = tuf.CHRCOD

        LEFT JOIN `ZCLF21_TEXT` tuc
            ON CAST(ma.ZZCLF21 AS STRING) = tuc.CHRCOD

        -- Product_Pack_Size: direct join from ZZCLF14
        LEFT JOIN dimensions_it_product_pack_size dpps
            ON CAST(ma.ZZCLF14 AS INT) = dpps.IT_Product_Pack_Size_ID

        -- Product_Category: direct join from ZZCLF12
        LEFT JOIN dimensions_it_product_category dpc
            ON CAST(ma.ZZCLF12 AS INT) = dpc.IT_Product_Category_ID

        -- EC_Group: ZREP uses ZZREPMATNR, others use MATNR_PK (material number)
        LEFT JOIN dimensions_item_taxonomy dt
            ON regexp_replace(ma.MATNR_PK,'^0+','') = regexp_replace(dt.Common_Item_ID,'^0+','')

        -- EC_Group Description
        LEFT JOIN dimensions_it_ec_group ecg
            ON dt.IT_EC_Group_ID = ecg.IT_EC_Group_ID

        -- Product_Segment: ZREP uses ZZREPMATNR, others use MATNR_PK (material number)
        LEFT JOIN dimensions_vw_item_product_category vw
            ON regexp_replace(ma.MATNR_PK,'^0+','') = regexp_replace(vw.Item_ID,'^0+','')
        """


class RETROFIT_API_PROCESS:
    LOGS = "snacking_eus2_{ENV}.mw_finance_mwd30anaplan.anaplan_api_logs"

    class ACTUALS:
        INPUT_DF = "actuals_output"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "81FBC1D4E213402C884C9E77279CDEA8"
        FILE_ID = "113000000194"
        PROCESS_ID = "118000000032"

    class PRODUCT_MASTER:
        INPUT_DF = "products_master"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "81FBC1D4E213402C884C9E77279CDEA8"
        FILE_ID = "113000000194"
        PROCESS_ID = "118000000037"

    class HEADCOUNT:
        INPUT_DF = "headcount_output"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "81FBC1D4E213402C884C9E77279CDEA8"
        FILE_ID = "113000000195"
        PROCESS_ID = "118000000033"

    class ACCOUNTS_MASTER:
        INPUT_DF = "accounts_master"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "81FBC1D4E213402C884C9E77279CDEA8"
        FILE_ID = "113000000106"
        PROCESS_ID = "118000000027"

    class ENTITY_HIER:
        INPUT_DF = "entity_hierarchy"
        WORKSPACE_ID = "8a868c7391de9ad901922ad284aa284c"
        MODEL_ID = "81FBC1D4E213402C884C9E77279CDEA8"
        FILE_ID = "113000000171"
        PROCESS_ID = "118000000030"


class TPM_PROCESSING:
    TPM_PROCESSING_OUTPUT = "df_trade_promo"

    # ── 1) NA Silver ─────────────────────────────────────────────────────────
    na_silver_query = """
            WITH cal_dedup AS (
                SELECT DISTINCT
                    GCALWKNY,
                    `0FISCYEAR`,
                    GMARSPINY
                FROM dim_calendar_tpm
            )
            SELECT
                CONCAT('P', CAST(cal.GMARSPINY AS INT), ' FY',
                    SUBSTRING(CAST(cal.`0FISCYEAR` AS STRING), 3, 2))           AS Fiscal_year_period,
                REGEXP_REPLACE(c.Plan_account_ID_new, '^0+', '')                   AS Plan_Account_ID,
                c.Plan_account_text_new                                             AS Plan_Account_Description,
                c.demand_group_kinaxis                                              AS Demand_group,
                c.demand_group_text_kinaxis                                         AS Demand_group_description,
                REGEXP_REPLACE(m.Rep_Item_ID, '^0+', '')                            AS ZERP,
                SUM(f.Total_Trade)                                                  AS Sales_Trade_Expenses_exc_NQC,
                c.Sales_Org,
                c.Distribution_Channel,
                c.Division
            FROM fact_account_plan f
            LEFT JOIN dim_cust_sales c
                ON f.customerKey = c.Cust_sales_KEY
            LEFT JOIN dim_material m
                ON REGEXP_REPLACE(m.`0MATERIAL`, '^0+', '') = f.productId
            LEFT JOIN cal_dedup cal
                ON f.marsYearWeek = cal.GCALWKNY
            WHERE
                f.Total_Trade IS NOT NULL
                AND c.Plan_Accounts IS NOT NULL
                AND c.Sales_Org IS NOT NULL
                AND f.Snapshot_type = 'LIVE'
            GROUP BY
                c.Sales_Org, c.Distribution_Channel, c.Division,
                c.Plan_account_ID_new, c.Plan_account_text_new,
                c.demand_group_kinaxis, c.demand_group_text_kinaxis,
                m.Rep_Item_ID, cal.`0FISCYEAR`, cal.GMARSPINY
            """

    # ── 2) CA ─────────────────────────────────────────────────────────────────
    ca_query = """
            WITH promo_agg AS (
                SELECT
                    Customer_Material_Key, year_week, sales_organisation,
                    SUM(COALESCE(MyCouponsandRedemptionsRetro, 0))      AS MyCouponsandRedemptionsRetro,
                    SUM(COALESCE(PrmSKUMyDisplayRetro, 0))              AS PrmSKUMyDisplayRetro,
                    SUM(COALESCE(`5772_TPR_budget_Plan_week`, 0))       AS `5772_TPR_budget_Plan_week`,
                    SUM(COALESCE(`6892_Assigned_Lumpsum_PLAN`, 0))      AS `6892_Assigned_Lumpsum_PLAN`,
                    SUM(COALESCE(MyTPRScanRetro, 0))                    AS MyTPRScanRetro
                FROM fact_internal_product_week
                WHERE sales_organisation LIKE '%121%'
                AND Business_Segment IN ('01','08')
                GROUP BY Customer_Material_Key, year_week, sales_organisation
            ),
            manual_agg AS (
                SELECT
                    Customer_Material_Key, MARS_Year_Period_Week, Sales_Organization,
                    SUM(COALESCE(MYCASHDISCOUNT, 0))            AS MYCASHDISCOUNT,
                    SUM(COALESCE(MYCOMBROKER, 0))               AS MYCOMBROKER,
                    SUM(COALESCE(CONSUMERPROMOTIONSRETRO, 0))   AS CONSUMERPROMOTIONSRETRO,
                    SUM(COALESCE(MYFREIGHTACCRUAL, 0))          AS MYFREIGHTACCRUAL,
                    SUM(COALESCE(MYPICKUPALLOWANCE, 0))         AS MYPICKUPALLOWANCE,
                    SUM(COALESCE(MYSALESVALUEFREEPRODUCT, 0))   AS MYSALESVALUEFREEPRODUCT
                FROM dim_manual_kpis
                WHERE Sales_Organization LIKE '%121%'
                AND Business_Segment IN ('01','08')
                GROUP BY Customer_Material_Key, MARS_Year_Period_Week, Sales_Organization
            ),
            cal_dedup AS (
                SELECT DISTINCT
                    GMARSYEAR * 100 + GMARSWINY  AS calendar_week,
                    GMARSYEAR                    AS mars_year,
                    GMARSPINY                    AS mars_period,
                    GCALWKNY
                FROM dim_calendar_tpm
            ),
            latest_snapshot AS (
                SELECT MAX(Snapshot_version) AS snap
                FROM fact_account_plan
                WHERE Snapshot_type = 'PERIODIC'
                AND salesorg LIKE '%121%'
                AND Business_Segment IN ('01','08')
            )
            SELECT
                CONCAT('P', CAST(cal.mars_period AS INT), ' FY',
                    SUBSTRING(CAST(cal.mars_year AS STRING), 3, 2))  AS Fiscal_year_period,
                REGEXP_REPLACE(c.Plan_account_ID_new, '^0+', '')        AS Plan_Account_ID,
                c.Plan_account_text_new                                 AS Plan_Account_Description,
                c.demand_group_kinaxis                                  AS Demand_group,
                c.demand_group_text_kinaxis                             AS Demand_group_description,
                REGEXP_REPLACE(m.Rep_Item_ID, '^0+', '')                AS ZERP,
                SUM(
                COALESCE(f.SegSKUMyAssortmentPlacementDiscountRetro, 0)
                + COALESCE(f.SegSKUMyCashDiscPlan, 0)
                + COALESCE(f.SegSKUMyClrnmrkdwnRetro, 0)
                + COALESCE(f.SegSKUMyConsumerPromotionsRetro, 0)
                + COALESCE(f.SegSKUMyCustomerLogisticsDiscountOI, 0)
                + COALESCE(f.SegSKUMyCustomerLogisticsDiscountRetro, 0)
                + COALESCE(f.SegSKUMyCustomerLogisticsPenaltyRetroPlan, 0)
                + COALESCE(f.SegSKUMyDisplayOI, 0)
                + COALESCE(f.SegSKUMyDisplayRetro, 0)
                + COALESCE(f.SegSKUMyEDLP1OI, 0)
                + COALESCE(f.SegSKUMyEDLP1Retro, 0)
                + COALESCE(f.SegSKUMyEDLP2OI, 0)
                + COALESCE(f.SegSKUMyEDLP2Retro, 0)
                + COALESCE(f.SegSKUMyFeatureRetro, 0)
                + COALESCE(f.SegSKUMyGrowthIncentivesRetro, 0)
                + COALESCE(f.SegSKUMyNonWorkingRetro, 0)
                + COALESCE(f.SegSKUMyNSROI, 0)
                + COALESCE(f.SegSKUMyNSRRetro, 0)
                + COALESCE(f.SegSKUMyTPROI, 0)
                + COALESCE(f.SegSKUMyTPRRetro, 0)
                + COALESCE(p.MyCouponsandRedemptionsRetro, 0)
                + COALESCE(p.PrmSKUMyDisplayRetro, 0)
                + COALESCE(p.`5772_TPR_budget_Plan_week`, 0)
                + COALESCE(p.`6892_Assigned_Lumpsum_PLAN`, 0)
                + COALESCE(p.MyTPRScanRetro, 0)
                + COALESCE(m2.MYCASHDISCOUNT, 0)
                + COALESCE(m2.MYCOMBROKER, 0)
                + COALESCE(m2.CONSUMERPROMOTIONSRETRO, 0)
                + COALESCE(m2.MYFREIGHTACCRUAL, 0)
                + COALESCE(m2.MYPICKUPALLOWANCE, 0)
                + COALESCE(m2.MYSALESVALUEFREEPRODUCT, 0)
                )                                                       AS Sales_Trade_Expenses_exc_NQC,
                '121'                                                   AS Sales_Org,
                c.Distribution_Channel,
                c.Division
            FROM fact_account_plan f
            CROSS JOIN latest_snapshot ls
            LEFT JOIN dim_cust_sales c
                ON f.customerKey = c.Cust_sales_KEY
            LEFT JOIN dim_material m
                ON REGEXP_REPLACE(m.`0MATERIAL`, '^0+', '') = f.productId
            LEFT JOIN cal_dedup cal
                ON f.marsYearWeek = cal.calendar_week
            LEFT JOIN promo_agg p
                ON f.Customer_Material_Key = p.Customer_Material_Key
                AND f.marsYearWeek = p.year_week
            LEFT JOIN manual_agg m2
                ON f.Customer_Material_Key = m2.Customer_Material_Key
                AND f.marsYearWeek = m2.MARS_Year_Period_Week
            WHERE f.salesorg LIKE '%121%'
            AND f.Snapshot_version = ls.snap
            AND c.Sales_Org IS NOT NULL
            AND Business_Segment IN ('01','08')
            GROUP BY
                c.Distribution_Channel, c.Division,
                c.Plan_account_ID_new, c.Plan_account_text_new,
                c.demand_group_kinaxis, c.demand_group_text_kinaxis,
                m.Rep_Item_ID, cal.mars_year, cal.mars_period
    """

    # ── Final select ──────────────────────────────────────────────────────────
    final_select = """
            SELECT
                CONCAT_WS('_', COALESCE(ZERP,'000'), COALESCE(Plan_Account_ID,'000'), COALESCE(Demand_group,'000'), COALESCE(Sales_Org,'000'), COALESCE(Distribution_Channel,'000')) AS unique_key,
                Fiscal_year_period,
                Plan_Account_ID AS `Plan Account ID`,
                Plan_Account_Description AS `Plan Account Description`,
                Demand_group,
                Demand_group_description,
                ZERP AS ZREP,
                Sales_Trade_Expenses_exc_NQC AS `Total Trade`,
                Sales_Org AS `Sales Org`,
                Distribution_Channel AS `Distribution Channel`,
                Division
            FROM tpm_combined
            """


class PRICE_PROCESSING:
    class STANDARD_COST:
        STANDARD_COST_QUERY = """

            WITH ranked AS (
            SELECT
                bukrs  AS Company_Code,
                werks  AS Plant,
                LTRIM('0', matnr) AS Material_Number,
                elemt  AS Cost_Component,
                statu  AS Costing_Status,
                meins  AS Unit_of_Measure,
                waers  AS Currency,
                CAST(wrtgs AS DOUBLE) AS Cost_Per_Case,
                CAST(losgr AS INT) AS Lot_Size,
                kadat  AS Costing_Date_From,
                bidat  AS Costing_Date_To,
                LOAD_DATE,
                ROW_NUMBER() OVER (
                    PARTITION BY werks, LTRIM('0', matnr), elemt
                    ORDER BY LOAD_DATE DESC
                ) AS rn
            FROM ZBW_CO_PC_PCP_20
            WHERE CURTP = '10'
            AND current_date() BETWEEN to_date(kadat, 'yyyy.MM.dd') AND to_date(bidat, 'yyyy.MM.dd')
        )
        SELECT
            CONCAT_WS('_', COALESCE(r.Company_Code,'000'), COALESCE(r.Plant,'000'), COALESCE(r.Material_Number,'000'), COALESCE(r.Cost_Component,'000'), COALESCE(r.Costing_Date_From,'000')) AS Code,
            r.Company_Code,
            r.Plant,
            r.Material_Number,
            r.Cost_Component,
            r.Costing_Status,
            r.Unit_of_Measure,
            r.Currency,
            r.Cost_Per_Case,
            r.Lot_Size,
            r.Costing_Date_From,
            r.Costing_Date_To,
            p.`Material_Type`   AS Material_Type,
            ct.TXTSH            AS Cost_Component_Description,
            p.`Material_Desc`   AS Material_Description,
            CAST(p.`Net_Weight` AS DOUBLE) AS Net_Weight,
            p.`Base_UOM`        AS Base_Unit,
            CASE WHEN CAST(p.`Net_Weight` AS DOUBLE) > 0
                THEN ROUND(r.Cost_Per_Case / CAST(p.`Net_Weight` AS DOUBLE), 4)
                ELSE NULL
            END AS Cost_Per_Tonne
        FROM ranked r
        LEFT JOIN (
            SELECT DISTINCT ELEMT_PK, TXTSH
            FROM 0COSTCOMP_TEXT
            WHERE LANGU_PK = 'EN' AND ELEHK_PK = 'Z2'
        ) ct ON r.Cost_Component = ct.ELEMT_PK
        LEFT JOIN (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY `Material_SKU` ORDER BY `Material_SKU`) AS prod_rn
            FROM product_master
        ) p ON r.Material_Number = p.`Material_SKU` AND p.prod_rn = 1
        WHERE r.rn = 1
        AND p.`Material_Type` = 'FERT'
                """

    class ICP:
        ICP_QUERY = """
            WITH a004_clean AS (
                SELECT DISTINCT
                    VKORG,
                    VTWEG,
                    regexp_replace(MATNR, '^0+', '') AS Matnr,
                    DATBI,
                    DATAB,
                    KNUMH
                FROM A004
            ),

            final_data AS (
                SELECT DISTINCT
                CONCAT_WS(
                    '_',
                    COALESCE(a.Matnr, '000'),
                    COALESCE(a.VKORG, '000'),
                    COALESCE(a.VTWEG, '000'),
                    COALESCE(a.DATAB, '000')
                ) AS unique_key,
                    a.Matnr       AS Material_Number,
                    p.Material_Desc AS Material_Description,
                    a.VKORG       AS Sales_Org,
                    a.VTWEG       AS Distribution_Channel,
                    a.DATAB       AS Start_Date,
                    a.DATBI       AS End_Date,
                    k.KMEIN       AS UOM,
                    k.KBETR       AS ICP
                FROM a004_clean a
                LEFT JOIN KONP k
                    ON a.KNUMH = k.KNUMH
                LEFT JOIN product_master p
                    ON a.Matnr = p.`Material_SKU`
            )

            SELECT
                unique_key,
                Material_Number,
                Material_Description,
                Sales_Org,
                Distribution_Channel,
                Start_Date,
                End_Date,
                UOM,
                ICP
            FROM final_data
            WHERE UOM IS NOT NULL
            ORDER BY Material_Number
            """

    class CUSTOMER_PRICE:
        CUSTOMER_PRICE_QUERY = """
            WITH product_map AS (
                SELECT
                    `Material_SKU` AS `Material_SKU`,
                    ZREP,
                    `ZREP_Desc`    AS ZREP_Desc
                FROM product_master
                WHERE ZREP IS NOT NULL
            ),

            base AS (
                SELECT
                    regexp_replace(a.MATNR, '^0+', '') AS ZREP,
                    a.VKORG, a.VTWEG, a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING) AS Demand_Group_ID,
                    CAST(NULL AS STRING) AS Demand_Group_Desc,
                    CAST(NULL AS STRING) AS SKU_original
                FROM A501 a
                WHERE a.KSCHL = 'PR00' AND a.VKORG = '239'

                UNION ALL

                SELECT
                    regexp_replace(a.MATNR, '^0+', ''),
                    a.VKORG, CAST(NULL AS STRING), CAST(NULL AS STRING),
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING)
                FROM A812 a
                WHERE a.KSCHL = 'ZPL0' AND a.VKORG = '239'

                UNION ALL

                SELECT
                    regexp_replace(a.MATNR, '^0+', ''),
                    a.VKORG, CAST(NULL AS STRING), CAST(NULL AS STRING),
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING)
                FROM A812 a
                WHERE a.KSCHL = 'ZR05' AND a.VKORG = '121'

                UNION ALL

                SELECT
                    regexp_replace(a.MATNR, '^0+', ''),
                    a.VKORG, a.VTWEG, CAST(NULL AS STRING),
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    c.`Demand Group`, c.`Demand Group Desc`, CAST(NULL AS STRING)
                FROM A872 a
                LEFT JOIN customer_master c
                    ON regexp_replace(a.KUNNR, '^0+', '') = c.Customer
                    AND a.VKORG = c.`Sales Org`
                    AND a.VTWEG = c.`Distribution Channel`
                WHERE a.KSCHL = 'ZR05' AND a.VKORG = '121'
                AND c.`Demand Group` IS NOT NULL

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, a.VTWEG, a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING)
                FROM A501 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                WHERE a.KSCHL = 'PR00' AND a.VKORG IN ('282','145','499','280','144')

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, a.VTWEG, a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    c.`Demand Group`, c.`Demand Group Desc`, CAST(NULL AS STRING)
                FROM A865 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                LEFT JOIN customer_master c
                    ON regexp_replace(a.KUNRG, '^0+', '') = c.Customer
                    AND a.VKORG = c.`Sales Org`
                    AND a.VTWEG = c.`Distribution Channel`
                WHERE a.KSCHL = 'PR00' AND a.VKORG IN ('282','145','499','280','144')
                AND c.`Demand Group` IS NOT NULL

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, a.VTWEG, a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), regexp_replace(a.MATNR, '^0+', '')
                FROM A501 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                WHERE a.KSCHL = 'ZM00' AND a.VKORG IN ('138','408','312')

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, CAST(NULL AS STRING), a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), regexp_replace(a.MATNR, '^0+', '')
                FROM A883 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                WHERE a.KSCHL = 'ZM00' AND a.VKORG IN ('138','408','312')

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, CAST(NULL AS STRING), a.PLTYP,
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    c.`Demand Group`, c.`Demand Group Desc`, regexp_replace(a.MATNR, '^0+', '')
                FROM A882 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                LEFT JOIN customer_master c
                    ON regexp_replace(a.KUNRG, '^0+', '') = c.Customer
                    AND a.VKORG = c.`Sales Org`
                WHERE a.KSCHL = 'ZM00' AND a.VKORG IN ('138','408','312')
                AND c.`Demand Group` IS NOT NULL

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, a.VTWEG, CAST(NULL AS STRING),
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    c.`Demand Group`, c.`Demand Group Desc`, CAST(NULL AS STRING)
                FROM A513 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                LEFT JOIN customer_master c
                    ON regexp_replace(a.KUNAG, '^0+', '') = c.Customer
                    AND a.VKORG = c.`Sales Org`
                    AND a.VTWEG = c.`Distribution Channel`
                WHERE a.KSCHL = 'PR00' AND a.VKORG IN ('282','145','499','280','144')
                AND c.`Demand Group` IS NOT NULL

                UNION ALL

                SELECT
                    COALESCE(p.ZREP, regexp_replace(a.MATNR, '^0+', '')),
                    a.VKORG, CAST(NULL AS STRING), CAST(NULL AS STRING),
                    a.DATAB, a.DATBI, a.KNUMH, a.KSCHL, a.MANDT, a.KAPPL,
                    CAST(NULL AS STRING), CAST(NULL AS STRING), CAST(NULL AS STRING)
                FROM A599 a
                LEFT JOIN product_map p ON regexp_replace(a.MATNR, '^0+', '') = p.Material_SKU
                WHERE a.KSCHL = 'PR00' AND a.VKORG IN ('282','145','499','280','144')
            ),

            joined AS (
                SELECT
                    b.ZREP, b.VKORG, b.VTWEG, b.PLTYP,
                    date_format(to_date(b.DATAB, 'yyyy.MM.dd'), 'yyyy.MM.dd') AS Start_Date,
                    date_format(to_date(b.DATBI, 'yyyy.MM.dd'), 'yyyy.MM.dd') AS End_Date,
                    b.KSCHL, b.Demand_Group_ID, b.Demand_Group_Desc,
                    k.KBETR, k.KONWA, k.KMEIN
                FROM base b
                INNER JOIN KONP k
                    ON b.KNUMH = k.KNUMH AND b.MANDT = k.MANDT
                    AND b.KAPPL = k.KAPPL AND b.KSCHL = k.KSCHL
                WHERE b.KSCHL <> 'ZM00'  AND k.KONWA IN ('USD', 'CAD')

                UNION ALL

                SELECT
                    b.ZREP, b.VKORG, b.VTWEG, b.PLTYP,
                    date_format(to_date(b.DATAB, 'yyyy.MM.dd'), 'yyyy.MM.dd') AS Start_Date,
                    date_format(to_date(b.DATBI, 'yyyy.MM.dd'), 'yyyy.MM.dd') AS End_Date,
                    b.KSCHL, b.Demand_Group_ID, b.Demand_Group_Desc,
                    CAST(l.effective_unit_price AS DOUBLE) AS KBETR,
                    'USD' AS KONWA,
                    'EA'  AS KMEIN
                FROM base b
                INNER JOIN (
                    SELECT part_name, effective_unit_price
                    FROM (
                        SELECT
                            part_name, effective_unit_price,
                            ROW_NUMBER() OVER (PARTITION BY part_name ORDER BY file_time_stamp DESC) AS rn
                        FROM edf_latam_csl_pricing_info
                    ) t
                    WHERE rn = 1
                ) l ON b.SKU_original = l.part_name
                WHERE b.KSCHL = 'ZM00'
            ),

            aggregated AS (
                SELECT
                    j.ZREP,
                    j.KSCHL                     AS Condition_Type,
                    ROUND(AVG(j.KBETR), 2)      AS Price,
                    j.KONWA                     AS Currency,
                    j.KMEIN                     AS UOM,
                    regexp_replace(j.Demand_Group_ID, '^0+', '') AS Demand_Group_ID,
                    j.Demand_Group_Desc,
                    j.Start_Date, j.End_Date,
                    j.VKORG                     AS Sales_Org,
                    j.VTWEG                     AS Distribution_Channel,
                    j.PLTYP                     AS Price_List
                FROM joined j
                GROUP BY
                    j.ZREP, j.KSCHL, j.KONWA, j.KMEIN,
                    regexp_replace(j.Demand_Group_ID, '^0+', ''), j.Demand_Group_Desc,
                    j.Start_Date, j.End_Date,
                    j.VKORG, j.VTWEG, j.PLTYP
            ),

            with_precedence AS (
                SELECT a.*,
                    MAX(CASE WHEN trim(coalesce(a.Demand_Group_ID, '')) <> '' THEN 1 ELSE 0 END)
                    OVER (
                        PARTITION BY
                            a.ZREP, a.Sales_Org, a.Condition_Type, a.Currency, a.UOM,
                            a.Start_Date, a.End_Date,
                            coalesce(a.Distribution_Channel, ''),
                            coalesce(a.Price_List, '')
                    ) AS has_dg_price
                FROM aggregated a
            ),

            filtered AS (
                SELECT * FROM with_precedence
                WHERE trim(coalesce(Demand_Group_ID, '')) <> '' OR has_dg_price = 0
            ),

            deduped AS (
                SELECT *,
                    MAX(CASE WHEN End_Date <> '9999.12.31' THEN 1 ELSE 0 END) OVER (
                        PARTITION BY
                            ZREP, Condition_Type, UOM, Start_Date,
                            Sales_Org, coalesce(Distribution_Channel, ''), coalesce(Demand_Group_ID, '')
                    ) AS has_specific_end,
                    COUNT(*) OVER (
                        PARTITION BY
                            ZREP, Condition_Type, UOM, Start_Date,
                            Sales_Org, coalesce(Distribution_Channel, ''), coalesce(Demand_Group_ID, '')
                    ) AS grp_cnt
                FROM filtered
            ),

            final_filtered AS (
                SELECT * FROM deduped
                WHERE grp_cnt = 1
                OR (grp_cnt > 1 AND (has_specific_end = 0 OR End_Date <> '9999.12.31'))
            ),

            zrep_desc AS (
                SELECT ZREP, MAX(ZREP_Desc) AS ZREP_Description
                FROM product_master
                WHERE ZREP IS NOT NULL
                GROUP BY ZREP
            )

            SELECT
                distinct

                     CONCAT(
                    f.ZREP, '_', f.Condition_Type, '_', coalesce(f.UOM, '000'), '_', coalesce(f.Demand_Group_ID, '000'), '_', f.Start_Date, '_', f.End_Date, '_', f.Sales_Org, '_',
                    coalesce(f.Distribution_Channel, '000'), '_', coalesce(f.Price_List, '000')
                ) AS unique_key,

                f.Condition_Type,
                f.ZREP,
                z.ZREP_Description,
                f.Price,
                f.Currency,
                f.UOM,
                f.Demand_Group_ID,
                f.Demand_Group_Desc,
                f.Start_Date,
                f.End_Date,
                f.Sales_Org,
                f.Distribution_Channel,
                ROUND(AVG(f.Price) OVER (PARTITION BY f.ZREP, coalesce(f.Demand_Group_ID, '')), 2) AS Price_List
            FROM final_filtered f
            LEFT JOIN zrep_desc z ON f.ZREP = z.ZREP
            ORDER BY f.ZREP, f.Condition_Type, f.Start_Date
        """


class UOM_PROCESSING:
    UOM_OUTPUT = "df_uom"

    UOM_QUERY = """
        WITH latest_uom AS (
            SELECT
                matnr,
                meinh,
                umrez,
                umren,
                gewei,
                zzntgew,
                ROW_NUMBER() OVER (
                    PARTITION BY matnr, meinh
                    ORDER BY effective_dt DESC
                ) AS rn
            FROM material_unit_conversions
        )

        SELECT
            p.`Material_SKU` AS Material_ID,
            p.`Base_UOM` AS Base_Unit,
            u.meinh AS To_Base_Unit,
            u.umrez AS Numerator_to_base_unit_Conversion,
            u.umren AS denominator_to_base_unit_conversion,
            u.gewei AS Base_Weight_Unit,
            u.zzntgew AS Net_Weight,
            p.`Traded_Unit_Format_Desc` AS TDU
        FROM product_master p
        LEFT JOIN latest_uom u
            ON regexp_replace(p.`Material_SKU`, '^0+', '') = regexp_replace(u.matnr, '^0+', '')
           AND u.rn = 1
    """


class ACTUALS_PROCESSING:
    ACTUALS_OUTPUT = "df_actuals"
    df_actuals = "df_actuals"

    customer_base_query = """
    SELECT /*+ BROADCAST(U_parent) BROADCAST(RL) BROADCAST(IT) BROADCAST(PL) */

        1                                               AS Submission_Type_ID,
        'Actuals'                                       AS Submission_Type,

        CONCAT(
            'P', CAST(SUBSTRING(CAST(F.Date_ID AS STRING), 5, 2) AS INT),
            ' FY', SUBSTRING(CAST(F.Date_ID AS STRING), 3, 2)
        )                                               AS Fiscal_Year_Period,

        F.Parent_Entity_ID                              AS Unit_ID,
        U_parent.Entity_Alias                           AS Unit_Description,

        F.Account_ID                                    AS Reporting_Line_ID,
        RL.Account_Alias                                AS Reporting_Line_Description,

        COALESCE(
            CAST(TRY_CAST(F.Item_ID AS BIGINT) AS STRING),
            F.Item_ID
        )                                               AS Common_Item_ID,
        IT.Description                                  AS Common_Item,

        COALESCE(
            CAST(TRY_CAST(IT.Representative_Material_ID AS BIGINT) AS STRING),
            IT.Representative_Material_ID
        )                                               AS Representative_Material_ID,
        PL.Material_Desc                                AS Representative_Material,

        F.Customer_ID,
        F.Customer_Entity_ID,
        F.Destination_Entity_ID,

        SUM(
            CASE
                WHEN RL.Account_Category_ID = 60 THEN F.Value
                WHEN C_CY.Plan_Rate IS NOT NULL  THEN F.Value * C_CY.Plan_Rate
                ELSE F.Value
            END
        )                                               AS Value

    FROM facts_financial_consolidated_customer F

    INNER JOIN entity_filters ef
        ON ef.Entity_ID = F.Parent_Entity_ID

    INNER JOIN ac_filters ac
        ON ac.Account_ID = F.Account_ID

    INNER JOIN dimensions_Entity U_parent
        ON U_parent.Entity_ID = F.Parent_Entity_ID

    INNER JOIN dimensions_Account RL
        ON RL.Account_ID = F.Account_ID

    INNER JOIN dimensions_Entity U1
        ON U1.Entity_ID = F.Source_Entity_ID

    LEFT JOIN dimensions_currency C_CY
        ON  C_CY.Currency_ID = U1.Currency_ID
        AND C_CY.FX_Type_ID = 2
        AND RL.Account_Category_ID <> 60

    LEFT JOIN dimensions_Item_Taxonomy IT
        ON IT.Common_Item_ID = F.Item_ID

    LEFT JOIN product_lookup PL
        ON TRY_CAST(PL.`Material_SKU` AS BIGINT)
         = TRY_CAST(IT.Representative_Material_ID AS BIGINT)

    WHERE F.Date_ID IN ({yearperiod})

    GROUP BY
        F.Date_ID,
        F.Parent_Entity_ID, U_parent.Entity_Alias,
        F.Account_ID,       RL.Account_Alias,
        F.Item_ID,          IT.Description,
        IT.Representative_Material_ID, PL.Material_Desc,
        F.Customer_ID,      F.Customer_Entity_ID,
        F.Destination_Entity_ID
    """

    ep_base_query = """
    SELECT /*+ BROADCAST(U_parent) BROADCAST(RL) BROADCAST(IT) BROADCAST(PL) */

        1                                               AS Submission_Type_ID,
        'Actuals'                                       AS Submission_Type,

        CONCAT(
            'P', CAST(SUBSTRING(CAST(F.Source_Date_ID AS STRING), 5, 2) AS INT),
            ' FY', SUBSTRING(CAST(F.Source_Date_ID AS STRING), 3, 2)
        )                                               AS Fiscal_Year_Period,

        F.Parent_Entity_ID                              AS Unit_ID,
        U_parent.Entity_Alias                           AS Unit_Description,

        F.Account_ID                                    AS Reporting_Line_ID,
        RL.Account_Alias                                AS Reporting_Line_Description,

        COALESCE(
            CAST(TRY_CAST(F.Item_ID AS BIGINT) AS STRING),
            F.Item_ID
        )                                               AS Common_Item_ID,
        IT.Description                                  AS Common_Item,

        COALESCE(
            CAST(TRY_CAST(IT.Representative_Material_ID AS BIGINT) AS STRING),
            IT.Representative_Material_ID
        )                                               AS Representative_Material_ID,
        PL.Material_Desc                                AS Representative_Material,

        CAST(NULL AS STRING)                             AS Customer_ID,
        CAST(NULL AS STRING)                             AS Customer_Entity_ID,
        CAST(NULL AS STRING)                             AS Destination_Entity_ID,

        SUM(
            CASE
                WHEN C.FX_Type_ID = 2
                    THEN F.Value * COALESCE(C.Plan_Rate, 1)
                WHEN C.FX_Type_ID IS NULL
                    THEN F.Value * COALESCE(C.Plan_Rate, 1)
                ELSE 0
            END
        )                                               AS Value

    FROM ep_account_entity F

    INNER JOIN entity_filters ef
        ON ef.Entity_ID = F.Parent_Entity_ID

    INNER JOIN rl_filters_ep rl_f
        ON rl_f.Account_ID = F.Account_ID

    INNER JOIN dimensions_Entity U_parent
        ON U_parent.Entity_ID = F.Parent_Entity_ID

    INNER JOIN dimensions_Account RL
        ON RL.Account_ID = F.Account_ID

    INNER JOIN dimensions_Entity U1
        ON U1.Entity_ID = F.Source_Entity_ID

    LEFT JOIN dimensions_currency C
        ON  C.Currency_ID = U1.Currency_ID
        AND C.FX_Type_ID IN (1, 2)
        AND RL.Account_Category_ID <> 60

    LEFT JOIN dimensions_Item_Taxonomy IT
        ON IT.Common_Item_ID = F.Item_ID

    LEFT JOIN product_lookup PL
        ON TRY_CAST(PL.`Material_SKU` AS BIGINT)
         = TRY_CAST(IT.Representative_Material_ID AS BIGINT)

    WHERE F.Source_Date_ID IN ({yearperiod})

    GROUP BY
        F.Source_Date_ID,
        F.Parent_Entity_ID, U_parent.Entity_Alias,
        F.Account_ID,       RL.Account_Alias,
        F.Item_ID,          IT.Description,
        IT.Representative_Material_ID, PL.Material_Desc
    """

    final_combined_query = """
    SELECT
        CONCAT(
            COALESCE(t.Submission_Type_ID,     '000'), '_',
            COALESCE(t.Unit_ID,                 '000'), '_',
            COALESCE(t.Reporting_Line_ID,        '000'), '_',
            COALESCE(t.Common_Item_ID,           '000'), '_',
            COALESCE(t.Customer_Destination_ID,  '000')
        )                                               AS Code,
        t.*
    FROM (
        SELECT /*+ BROADCAST(Cust) BROADCAST(Dest_E) BROADCAST(CD) */
            1                                           AS Submission_Type_ID,
            'Actuals'                                   AS Submission_Type,
            cb.Fiscal_Year_Period,
            cb.Unit_ID,
            cb.Unit_Description,
            cb.Reporting_Line_ID,
            cb.Reporting_Line_Description,
            cb.Common_Item_ID,
            cb.Common_Item,
            cb.Representative_Material_ID,
            cb.Representative_Material,

            CASE WHEN cb.Reporting_Line_ID IN ('S900122','FR4300')
                 THEN NULL ELSE Cust.KUNNR
            END                                         AS Customer_ID,
            CASE WHEN cb.Reporting_Line_ID IN ('S900122','FR4300')
                 THEN NULL ELSE CD.Customer_Description
            END                                         AS Customer_Description,

            CASE WHEN cb.Reporting_Line_ID IN ('S900122','FR4300')
                 THEN cb.Destination_Entity_ID ELSE NULL
            END                                         AS Destination_ID,

            CASE WHEN cb.Reporting_Line_ID IN ('S900122','FR4300')
                 THEN Dest_E.Entity_Alias      ELSE NULL
            END                                         AS Destination_Description,

            CASE WHEN cb.Reporting_Line_ID IN ('S900122','FR4300')
                 THEN cb.Destination_Entity_ID ELSE Cust.KUNNR
            END                                         AS Customer_Destination_ID,

            cb.Value

        FROM combined_base cb

        LEFT JOIN dimensions_customer Cust
            ON  Cust.Customer_ID = cb.Customer_ID
            AND Cust.Entity_ID   = cb.Customer_Entity_ID

        LEFT JOIN dimensions_Entity Dest_E
            ON Dest_E.Entity_ID = cb.Destination_Entity_ID

        LEFT JOIN customer_dedup CD
            ON CAST(CD.Customer AS STRING) = Cust.KUNNR
    ) t
    """


class ACTUALS_RAW:
    """
    Config for materialising the filtered source facts into the RAW zone.

    ACTUALS_PROCESS reads its ``facts_financial_consolidated_customer`` and
    ``ep_account_entity`` inputs from these RAW parquet locations, so
    ACTUALS_RAW_PROCESS must run and complete before ACTUALS_PROCESS.
    """

    # Output DataFrame names. The RAW zone write paths, partition columns and
    # dynamic-overwrite behaviour now live in the file_writer `output` entries of
    # ACTUALS_RAW_PROCESS in project_config.json; these names must match the
    # `dataframe_name` of those outputs. They also stay in sync with the
    # file_reader inputs of ACTUALS_PROCESS.
    CUSTOMER_OUTPUT = "customer_raw_output"
    EP_OUTPUT = "ep_raw_output"

    customer_query = """
    SELECT *
    FROM raw_customer_source
    WHERE Account_ID IN ({account_list})
      AND Parent_Entity_ID IN ({entity_list})
      AND Date_ID IN ({yearperiod})
    """

    ep_query = """
    SELECT *
    FROM raw_ep_source
    WHERE Account_ID IN ({account_list_ep})
      AND Parent_Entity_ID IN ({entity_list})
      AND Source_Date_ID IN ({yearperiod})
    """


class SUPPLY_PROCESSING:
    SUPPLY_OUTPUT = "df_supply"

    despatched_na_query = """
        WITH latest_despatched AS (
        -- Lock snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM Despatched
        WHERE as_of_dt = (
            SELECT MAX(as_of_dt) FROM Despatched
            WHERE as_of_dt <= '{process_date}'
        )
        ),
        agg_despatched_na AS (
        SELECT
            d.PART_PART, d.PART_DESCRIPTION, d.SOURCE_SITE, d.PART_SITE,
            CONCAT('P', CAST(cal.periodnumber AS STRING), ' FY', SUBSTRING(CAST(cal.marsyear AS STRING), 3, 2)) AS fiscal_year_period,
            SUM(CAST(d.QUANTITY AS DOUBLE)) AS QUANTITY
        FROM latest_despatched d
        LEFT JOIN mars_calendar cal ON CAST(d.DUE_DATE AS DATE) = cal.Date
        GROUP BY d.PART_PART, d.PART_DESCRIPTION, d.SOURCE_SITE, d.PART_SITE,
            CONCAT('P', CAST(cal.periodnumber AS STRING), ' FY', SUBSTRING(CAST(cal.marsyear AS STRING), 3, 2))
        )
        SELECT
        'ForecastDespatched'                     AS Demand_Type,
        p.PART_SITE                              AS Part_Site,
        p.SOURCE_SITE                            AS Destination_Site,
        p.PART_PART                              AS Material_Number,
        p.PART_DESCRIPTION                       AS Material_Description,
        mm.ZREP,
        p.fiscal_year_period                     AS Fiscal_year_period,
        COALESCE(ROUND(CAST(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN p.QUANTITY
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN p.QUANTITY
            WHEN bu.Base_Unit = 'EA' THEN p.QUANTITY * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE p.QUANTITY * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END AS DOUBLE), 0), 0)                 AS volume_cases,
        ROUND(p.QUANTITY * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS volume_tonnes,
        so.sales_org                             AS Sales_org
        FROM agg_despatched_na p
        LEFT JOIN v_ea_to_cs cs       ON p.PART_PART = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg      ON p.PART_PART = ekg.Material_ID
        LEFT JOIN v_base_uom bu       ON p.PART_PART = bu.Material_ID
        LEFT JOIN v_material_tdu tdu  ON p.PART_PART = tdu.Material_ID
        LEFT JOIN v_material_master mm ON p.PART_PART = mm.Material_SKU
        LEFT JOIN salesorg so         ON p.SOURCE_SITE = TRIM(so.`site`)
        """

    despatched_latam_query = """
        WITH latest_latam AS (
        -- Lock snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM df_latam
        WHERE as_of_dt = (
            SELECT MAX(as_of_dt) FROM df_latam
            WHERE as_of_dt <= '{process_date}'
        )
        ),
        agg_despatched_latam AS (
        SELECT
            l.type,
            l.part_site_value,
            l.part_name,
            l.part_description,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2)) AS fiscal_year_period,
            SUM(l.demand_qty) AS quantity
        FROM latest_latam l
        LEFT JOIN mars_calendar cal ON CAST(l.due_date AS DATE) = cal.Date
        WHERE l.type LIKE '%Allocation%'
            AND l.part_source_type_value = 'Transfer'
        GROUP BY l.type, l.part_site_value, l.part_name, l.part_description,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2))
        )
        SELECT
        l.type                                   AS Demand_Type,
        l.part_site_value                        AS Part_Site,
        NULL                                     AS Destination_Site,
        l.part_name                              AS Material_Number,
        l.part_description                       AS Material_Description,
        mm.ZREP,
        l.fiscal_year_period                     AS Fiscal_year_period,
        COALESCE(ROUND(CAST(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN l.quantity
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN l.quantity
            WHEN bu.Base_Unit = 'EA' THEN l.quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE l.quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END AS DOUBLE), 0), 0)                 AS volume_cases,
        ROUND(l.quantity * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS volume_tonnes,
        so.sales_org                             AS Sales_org
        FROM agg_despatched_latam l
        LEFT JOIN v_ea_to_cs cs        ON l.part_name = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg       ON l.part_name = ekg.Material_ID
        LEFT JOIN v_base_uom bu        ON l.part_name = bu.Material_ID
        LEFT JOIN v_material_tdu tdu   ON l.part_name = tdu.Material_ID
        LEFT JOIN v_material_master mm ON l.part_name = mm.Material_SKU
        LEFT JOIN salesorg so          ON l.part_site_value = TRIM(so.`site`)
        """

    production_na_query = """
        WITH latest_prod_unit AS (
        -- Lock snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM production_Volumes_unit
        WHERE as_of_dt = (
            SELECT MAX(as_of_dt) FROM production_Volumes_unit
            WHERE as_of_dt <= '{process_date}'
        )
        ),
        latest_prod_tonnes AS (
        -- Lock snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM production_Volumes_tonnes
        WHERE as_of_dt = (
            SELECT MAX(as_of_dt) FROM production_Volumes_tonnes
            WHERE as_of_dt <= '{process_date}'
        )
        ),
        agg_prod_unit AS (
        SELECT
            u.M_PART_PART, u.DESCRIPTION, u.M_SITE_SITE,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2)) AS fiscal_year_period,
            SUM(CAST(u.QUANTITY AS DOUBLE)) AS QUANTITY
        FROM latest_prod_unit u
        LEFT JOIN mars_calendar cal ON CAST(u.DUE_DATE AS DATE) = cal.Date
        GROUP BY u.M_PART_PART, u.DESCRIPTION, u.M_SITE_SITE,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2))
        ),
        agg_prod_tonnes AS (
        SELECT
            t.M_PART_PART, t.M_SITE_SITE,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2)) AS fiscal_year_period,
            SUM(CAST(t.QUANTITY_IN_TONNES AS DOUBLE)) AS QUANTITY_IN_TONNES
        FROM latest_prod_tonnes t
        LEFT JOIN mars_calendar cal ON CAST(t.DUE_DATE AS DATE) = cal.Date
        GROUP BY t.M_PART_PART, t.M_SITE_SITE,
            CONCAT('P', CAST(cal.PeriodNumber AS STRING), ' FY', SUBSTRING(CAST(cal.MarsYear AS STRING), 3, 2))
        )
        SELECT
        'ForecastProduction'                     AS Demand_Type,
        u.M_SITE_SITE                            AS Part_Site,
        NULL                                     AS Destination_Site,
        u.M_PART_PART                            AS Material_Number,
        u.DESCRIPTION                            AS Material_Description,
        mm.ZREP,
        u.fiscal_year_period                     AS Fiscal_year_period,
        COALESCE(ROUND(CAST(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN u.QUANTITY
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN u.QUANTITY
            WHEN bu.Base_Unit = 'EA' THEN u.QUANTITY * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE u.QUANTITY * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END AS DOUBLE), 0), 0)                 AS volume_cases,
        ROUND(t.QUANTITY_IN_TONNES, 6)           AS volume_tonnes,
        so.sales_org                             AS Sales_org
        FROM agg_prod_unit u
        INNER JOIN agg_prod_tonnes t
        ON u.M_PART_PART = t.M_PART_PART
        AND u.M_SITE_SITE = t.M_SITE_SITE
        AND u.fiscal_year_period = t.fiscal_year_period
        LEFT JOIN v_ea_to_cs cs       ON u.M_PART_PART = cs.Material_ID
        LEFT JOIN v_base_uom bu       ON u.M_PART_PART = bu.Material_ID
        LEFT JOIN v_material_tdu tdu  ON u.M_PART_PART = tdu.Material_ID
        LEFT JOIN v_material_master mm ON u.M_PART_PART = mm.Material_SKU
        LEFT JOIN salesorg so         ON u.M_SITE_SITE = TRIM(so.`site`)
        """

    production_latam_query = """
        WITH latest_latam AS (
        -- Lock snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM df_latam
        WHERE as_of_dt = (
                   SELECT MAX(as_of_dt) FROM df_latam
                   WHERE as_of_dt <= '{process_date}'
               )
        ),
        agg_prod_latam AS (
        SELECT
            l.type,
            l.part_site_value,
            l.part_name,
            l.part_description,
            CONCAT('P', CAST(cal.periodnumber AS STRING), ' FY', SUBSTRING(CAST(cal.marsyear AS STRING), 3, 2)) AS fiscal_year_period,
            SUM(l.supply_qty) AS quantity
        FROM latest_latam l
        LEFT JOIN mars_calendar cal ON CAST(l.due_date AS DATE) = cal.Date
        WHERE l.type IN ('ScheduledReceipt', 'PlannedOrder')
            AND l.part_source_type_value = 'Make'
        GROUP BY l.type, l.part_site_value, l.part_name, l.part_description,
            CONCAT('P', CAST(cal.periodnumber AS STRING), ' FY', SUBSTRING(CAST(cal.marsyear AS STRING), 3, 2))
        )
        SELECT
        l.type                                   AS Demand_Type,
        l.part_site_value                        AS Part_Site,
        NULL                                     AS Destination_Site,
        l.part_name                              AS Material_Number,
        l.part_description                       AS Material_Description,
        mm.ZREP,
        l.fiscal_year_period                     AS Fiscal_year_period,
        COALESCE(ROUND(CAST(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN l.quantity
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN l.quantity
            WHEN bu.Base_Unit = 'EA' THEN l.quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE l.quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END AS DOUBLE), 0), 0)                 AS volume_cases,
        ROUND(l.quantity * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS volume_tonnes,
        so.sales_org                                              AS Sales_org
        FROM agg_prod_latam l
        LEFT JOIN v_ea_to_cs cs        ON l.part_name = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg       ON l.part_name = ekg.Material_ID
        LEFT JOIN v_base_uom bu        ON l.part_name = bu.Material_ID
        LEFT JOIN v_material_tdu tdu   ON l.part_name = tdu.Material_ID
        LEFT JOIN v_material_master mm ON l.part_name = mm.Material_SKU
        LEFT JOIN salesorg so          ON l.part_site_value = TRIM(so.`site`)
        """


class DEMAND_PROCESSING:
    DEMAND_OUTPUT = "df_demand"

    na_query = """
        WITH lock_snapshot_usmw AS (
            -- Sales Org 239 (USMW): lock on prior period end snapshot = process_date - 10 days
            SELECT MAX(snapshot_date) AS snap FROM comb_na
            WHERE location = 'USMW'
                AND snapshot_date <= DATE_ADD('{process_date}', -10)
        ),
        lock_snapshot_camw AS (
            -- Sales Org 121 (CAMW): lock on period start (W1 Sunday) = process_date - 9 days
            SELECT MAX(snapshot_date) AS snap FROM comb_na
            WHERE location = 'CAMW'
                AND snapshot_date <= DATE_ADD('{process_date}', -9)
        ),

        latest_na AS (
        SELECT c.*, d.effective_unit_price
        FROM comb_na c
        LEFT JOIN na_consensus d
            ON  c.material_number = d.material_number
            AND c.location        = d.location
            AND c.demand_group    = d.demand_group
            AND c.start_date      = d.start_date
            AND c.snapshot_date   = d.snapshot_date
        WHERE c.location IN ('USMW', 'CAMW')
            AND (
            (c.location = 'USMW' AND c.snapshot_date = (SELECT snap FROM lock_snapshot_usmw))
            OR
            (c.location = 'CAMW' AND c.snapshot_date = (SELECT snap FROM lock_snapshot_camw))
            )
        ),
        agg_na AS (
        SELECT
            n.material_number, n.location, n.demand_group,
            n.forecast_type, n.sub_category_value,
            cal.MarsYearPeriod AS fiscal_year_period,
            SUM(n.forecast_quantity)      AS forecast_quantity,
            SUM(CASE WHEN n.forecast_type = 'FinalForecast' THEN n.forecast_quantity * n.effective_unit_price END) AS gsv
        FROM latest_na n
        LEFT JOIN marscal cal ON n.start_date = cal.Date
        GROUP BY n.material_number, n.location, n.demand_group,
                n.forecast_type, n.sub_category_value, cal.MarsYearPeriod
        )
        SELECT
        a.material_number                        AS Material_Number,
        p.Material_Desc                          AS Material_Description,
        a.location                               AS Site,
        CONCAT('P', CAST(SUBSTRING(a.fiscal_year_period, 6, 2) AS INT), ' FY', SUBSTRING(a.fiscal_year_period, 3, 2)) AS Fiscal_year_period,
        NULL                                     AS Customer_ID,
        NULL                                     AS Customer_Description,
        a.demand_group                           AS Demand_group,
        c.`Demand Group Desc`                    AS Demand_group_description,
        fm.ForecastTypeID                        AS Forecast_Type_ID,
        a.forecast_type                          AS Forecast_Type,
        bm.BB_ID                                 AS Building_Block_ID,
        a.sub_category_value                     AS Building_Block,
        ROUND(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' THEN a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END, 0)                                AS Volume_cases,
        ROUND(a.forecast_quantity * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS Volume_tonnes,
        a.gsv                                    AS GSV,
        so.sales_org                             AS Sales_org,
        c.`Distribution Channel`                 AS Distribution_Channel,
        c.Division                               AS Division
        FROM agg_na a
        LEFT JOIN salesorg so        ON a.location        = so.`site`
        LEFT JOIN v_customer_by_dg c ON a.demand_group    = c.`Demand Group`
                                    AND c.`Sales Org`    = CAST(so.sales_org AS STRING)
        LEFT JOIN v_product p        ON a.material_number = p.Material_SKU
        LEFT JOIN v_ea_to_cs cs      ON a.material_number = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg     ON a.material_number = ekg.Material_ID
        LEFT JOIN v_base_uom bu      ON a.material_number = bu.Material_ID
        LEFT JOIN v_material_tdu tdu ON a.material_number = tdu.Material_ID
        LEFT JOIN forecast_mapping fm ON COALESCE(a.forecast_type, '') = fm.ForecastType
        LEFT JOIN BB_mapping bm      ON COALESCE(a.sub_category_value, '') = bm.BB
            """

    latm_con_query = """
          WITH latest_latm AS (
        -- Lock LATM snapshot to latest as_of_dt on or before W2 Tuesday
        SELECT *
        FROM latm_consensus
        WHERE as_of_dt = (
            SELECT MAX(as_of_dt) FROM latm_consensus
            WHERE as_of_dt <= '{process_date}'
        )
        ),
        agg_latm AS (
        SELECT
            l.zrep AS material_number,
            l.part_site AS location,
            SPLIT(l.part_customer_customer_id, '_')[0] AS parsed_cust_id,
            SPLIT(l.part_customer_customer_id, '_')[3] AS division,
            cal.MarsYearPeriod AS fiscal_year_period,
            SUM(l.quantity)                              AS forecast_quantity,
            SUM(l.quantity * l.effective_unit_price)     AS gsv
        FROM latest_latm l
        LEFT JOIN marscal cal ON l.date = cal.Date
        GROUP BY l.zrep, l.part_site,
                SPLIT(l.part_customer_customer_id, '_')[0],
                SPLIT(l.part_customer_customer_id, '_')[3],
                cal.MarsYearPeriod
        )
        SELECT
        a.material_number                        AS Material_Number,
        p.Material_Desc                          AS Material_Description,
        a.location                               AS Site,
        CONCAT('P', CAST(SUBSTRING(a.fiscal_year_period, 6, 2) AS INT), ' FY', SUBSTRING(a.fiscal_year_period, 3, 2)) AS Fiscal_year_period,
        a.parsed_cust_id                         AS Customer_ID,
        ci.`Customer Desc`                       AS Customer_Description,
        ci.`Demand Group`                        AS Demand_group,
        ci.`Demand Group Desc`                   AS Demand_group_description,
        fm.ForecastTypeID                        AS Forecast_Type_ID,
        'FinalForecast'                          AS Forecast_Type,
        bm.BB_ID                                 AS Building_Block_ID,
        'FinalForecast'                          AS Building_Block,
        ROUND(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' THEN a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END, 0)                                AS Volume_cases,
        ROUND(a.forecast_quantity * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS Volume_tonnes,
        a.gsv                                    AS GSV,
        so.sales_org                             AS Sales_org,
        ci.`Distribution Channel`                AS Distribution_Channel,
        a.division                               AS Division
        FROM agg_latm a
        LEFT JOIN salesorg so        ON a.location         = so.`site`
        LEFT JOIN v_customer_by_id ci ON CAST(a.parsed_cust_id AS INT) = ci.Customer
                                    AND ci.`Sales Org`   = CAST(so.sales_org AS STRING)
        LEFT JOIN v_product p        ON a.material_number  = p.Material_SKU
        LEFT JOIN v_ea_to_cs cs      ON a.material_number  = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg     ON a.material_number  = ekg.Material_ID
        LEFT JOIN v_base_uom bu      ON a.material_number  = bu.Material_ID
        LEFT JOIN v_material_tdu tdu ON a.material_number  = tdu.Material_ID
        LEFT JOIN forecast_mapping fm ON 'FinalForecast'   = fm.ForecastType
        LEFT JOIN BB_mapping bm      ON 'FinalForecast'    = bm.BB
    """

    latm_pre_query = """

        WITH latest_latm AS (
                -- Lock LATM snapshot to latest as_of_dt on or before W2 Tuesday
                SELECT *
                FROM latm_preconsensus
                WHERE as_of_dt = (
                    SELECT MAX(as_of_dt) FROM latm_preconsensus
                    WHERE as_of_dt <= '{process_date}'
                )
                ),
        agg_latm AS (
        SELECT
            l.zrep                                 AS material_number,
            l.part_site                            AS location,
            SPLIT(l.customer_id, '_')[0]           AS customer_key,
            SPLIT(l.customer_id, '_')[3]           AS division,
            NULL                                   AS forecast_type,
            l.forecast_category                    AS sub_category_value,
            cal.MarsYearPeriod                     AS fiscal_year_period,
            SUM(CAST(l.quantity AS DOUBLE))        AS forecast_quantity
        FROM latest_latm l
        LEFT JOIN marscal cal ON l.date = cal.Date
        GROUP BY
            l.zrep,
            l.part_site,
            SPLIT(l.customer_id, '_')[0],
            SPLIT(l.customer_id, '_')[3],
            l.forecast_category,
            cal.MarsYearPeriod
        )
        SELECT
        a.material_number                        AS Material_Number,
        p.Material_Desc                          AS Material_Description,
        a.location                               AS Site,
        CONCAT('P', CAST(SUBSTRING(a.fiscal_year_period, 6, 2) AS INT), ' FY', SUBSTRING(a.fiscal_year_period, 3, 2)) AS Fiscal_year_period,
        a.customer_key                           AS Customer_ID,
        ci.`Customer Desc`                       AS Customer_Description,
        ci.`Demand Group`                        AS Demand_group,
        ci.`Demand Group Desc`                   AS Demand_group_description,
        fm.ForecastTypeID                        AS Forecast_Type_ID,
        a.forecast_type                          AS Forecast_Type,
        bm.BB_ID                                 AS Building_Block_ID,
        a.sub_category_value                     AS Building_Block,
        ROUND(
            CASE
            WHEN bu.Base_Unit = 'CS' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' AND UPPER(tdu.TDU) LIKE '%CASE%' THEN a.forecast_quantity
            WHEN bu.Base_Unit = 'EA' THEN a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            ELSE a.forecast_quantity * COALESCE(cs.num / NULLIF(cs.den, 0), 1)
            END, 0)                                AS Volume_cases,
        ROUND(a.forecast_quantity * COALESCE(ekg.kg_per_ea, 0) * 0.001, 6) AS Volume_tonnes,
        CAST(NULL AS DOUBLE)                     AS GSV,
        so.sales_org                             AS Sales_org,
        ci.`Distribution Channel`                AS Distribution_Channel,
        a.division                               AS Division
        FROM agg_latm a
        LEFT JOIN salesorg so        ON a.location         = so.`site`
        LEFT JOIN v_customer_by_id ci ON CAST(a.customer_key AS INT) = ci.Customer
                                    AND ci.`Sales Org`   = CAST(so.sales_org AS STRING)
        LEFT JOIN v_product p        ON a.material_number  = p.Material_SKU
        LEFT JOIN v_ea_to_cs cs      ON a.material_number  = cs.Material_ID
        LEFT JOIN v_ea_to_kg ekg     ON a.material_number  = ekg.Material_ID
        LEFT JOIN v_base_uom bu      ON a.material_number  = bu.Material_ID
        LEFT JOIN v_material_tdu tdu ON a.material_number  = tdu.Material_ID
        LEFT JOIN forecast_mapping fm ON COALESCE(a.forecast_type, '') = fm.ForecastType
        LEFT JOIN BB_mapping bm      ON COALESCE(a.sub_category_value, '') = bm.BB
    """

    cca_demand_query = """
            SELECT
        CAST(c.ZREP AS STRING)                   AS Material_Number,
        p.Material_Desc                        AS Material_Description,
        NULL                                     AS Site,
        CONCAT('P', CAST(SUBSTRING(c.Fiscal_year_period, 2, 2) AS INT), ' FY', SUBSTRING(c.Fiscal_year_period, 7, 2)) AS Fiscal_year_period,
        NULL                                     AS Customer_ID,
        NULL                                     AS Customer_Description,
        CAST(c.demand_group_id AS STRING)        AS Demand_group,
        c.Demand_group_description               AS Demand_group_description,
        fm.ForecastTypeID                        AS Forecast_Type_ID,
        NULL                                     AS Forecast_Type,
        bm.BB_ID                                 AS Building_Block_ID,
        c.Building_Block                         AS Building_Block,
            COALESCE(ROUND(CAST(c.cases AS DOUBLE), 0), 0)        AS Volume_cases,
            COALESCE(ROUND(CAST(c.tonnes AS DOUBLE), 2), 0)        AS Volume_tonnes,
        CAST(NULL AS DOUBLE)                     AS GSV,
        CAST(c.`Sales_Org` AS STRING)            AS Sales_org,
        NULL                                     AS Distribution_Channel,
        NULL                                     AS Division
        FROM cca c
        LEFT JOIN forecast_mapping fm ON '' = fm.ForecastType
        LEFT JOIN BB_mapping bm  ON COALESCE(c.Building_Block, '') = bm.BB

        LEFT JOIN (
            SELECT
                Material_SKU,
                MAX(Material_Desc) AS Material_Desc
            FROM product
            GROUP BY Material_SKU
        ) p
            ON p.Material_SKU = c.ZREP
    """


class PROCESSING_CONST:
    MATERIAL_NUMBER = "Material_Number"
    SALES_ORG = "Sales_org"
    PART_SITE = "Part_Site"
    DEMAND_TYPE = "Demand_Type"
    DESTINATION_SITE = "Destination_Site"
    UNIQUE_KEY = "unique_key"
    MATERIAL_DESCRIPTION = "Material_Description"
    ZREP = "ZREP"
    FISCAL_YEAR_PERIOD = "Fiscal_year_period"
    VOLUME_CASES = "volume_cases"
    VOLUME_TONNES = "volume_tonnes"
    # ── Demand columns ────────────────────────────────────────────────────────
    SITE = "Site"
    CUSTOMER_ID = "Customer_ID"
    CUSTOMER_DESCRIPTION = "Customer_Description"
    DEMAND_GROUP = "Demand_group"
    DEMAND_GROUP_DESCRIPTION = "Demand_group_description"
    FORECAST_TYPE_ID = "Forecast_Type_ID"
    FORECAST_TYPE = "Forecast_Type"
    BUILDING_BLOCK_ID = "Building_Block_ID"
    BUILDING_BLOCK = "Building_Block"
    DISTRIBUTION_CHANNEL = "Distribution_Channel"
    DIVISION = "Division"
    GSV = "GSV"
    # ── Actuals columns ───────────────────────────────────────────────────────
    ENTITY_ID = "entity_id"
    CUSTOMER = "Customer"
    CODE = "Code"
    FISCAL_YEAR_PERIOD_CAPS = "Fiscal_Year_Period"
    VALUE = "Value"
    DEFAULT_ZERO_3 = "000"
    # Mars calendar: a fiscal year holds 13 periods (P1..P13).
    MARS_PERIODS_PER_YEAR = 13
    # Rolling window used by the forward looking assets (TPM, Supply, Demand):
    # the current Mars period plus the next 17 periods, so 18 periods in total.
    FORWARD_PERIODS_AHEAD = 17
    MARS_CALENDAR_DF = "mars_cal"

