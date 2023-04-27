<template>
    <v-row justify="center">
      <v-dialog v-model="draftsDialog" max-width="800px">
        <!-- <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">Open Dialog</v-btn>
        </template>-->
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Denomination')
            }}</span>
          </v-card-title>
          <v-row>
            <v-container>
              
                <v-col cols="12">
                <template>
                  <!-- <v-data-table
                    :headers="denomination_headers"
                    :items="denomination_data"
                    item-key="currency"
                    class="elevation-1"
                    :items-per-page="itemsPerPage"
                    hide-default-footer
                    v-model="table"
                  >
                    <template v-slot:item.amount="props">
                      <v-edit-dialog :return-value.sync="props.item.amount">
                        {{ props.item.amount }}
                        <template v-slot:input>
                          <v-text-field
                            v-model="props.item.amount"
                            :rules="[max25chars]"
                            :label="frappe._('Edit')"
                            single-line
                            counter
                            type="number"
                           
                          ></v-text-field>
                        </template>
                      </v-edit-dialog>
                    </template>

                    <template v-slot:item.count="props">
                    <v-edit-dialog :return-value.sync="props.item.count">
                      {{ props.item.count }}
                      <template v-slot:input>
                        <v-text-field
                          v-model="props.item.count"
                          :rules="[max25chars]"
                          :label="frappe._('Edit')"
                          single-line
                          counter
                          type="number"
                          @change="update_amount($event,props.item)"
                        ></v-text-field>

                      </template>
                    </v-edit-dialog>
                  </template>
                  </v-data-table> -->
                  <v-simple-table>
                      <template v-slot:default>
                        <thead>
                          <tr>
                            <th class="text-center" width='100px'>
                              Currency
                            </th>
                            <th class="text-center" width='100px'>
                              Count
                            </th>
                            <th class="text-center" width='100px'>
                              Amount
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                          v-for="items in denomination_data"
                          :key="items.currency">
                            <td><v-text-field placeholder="Currency" v-model="items.currency" dense readonly></v-text-field></td>
                            <td><v-text-field placeholder="Count" v-model="items.count" dense @change="update_amount($event,items)"></v-text-field></td>
                            <td><v-text-field placeholder="Amount" v-model="items.amount" dense readonly></v-text-field></td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>
                </template>

              </v-col>
                <v-col cols="12">
                <template>

                  <v-row>
                    <v-col col = 4>
                      <v-text-field
                      dense
                      outlined
                      color="primary"
                      :label="frappe._('Total Amount')"
                      background-color="white"
                      hide-details
                      v-model="grand_amount"
                    
                      type="number"
                    ></v-text-field>
                    <v-text-field
                      dense
                      outlined
                      color="primary"
                      :label="frappe._('Difference')"
                      background-color="white"
                      hide-details
                      v-model="diff_amount"
                      
                    
                      type="number"
                    ></v-text-field>
                    <v-text-field
                      dense
                      outlined
                      color="primary"
                      :label="frappe._('Change Given')"
                      background-color="white"
                      hide-details
                      v-model="change_total_amount"
                      
                      type="number"
                     
                    ></v-text-field>
                    </v-col>
                  </v-row>
         
                  <v-card-title>
            <span class="headline primary--text">{{
              __('Change')
            }}</span>
          </v-card-title>
                  <!-- <v-data-table
                    :headers="change_footer"
                    :items="change_denomination_data"
                    item-key="currency"
                    class="elevation-1"
                    :items-per-page="itemsPerPage"
                    hide-default-footer
                    v-model="table"
                  >
                    <template v-slot:item.amount="props">
                      <v-edit-dialog :return-value.sync="props.item.amount">
                        {{ props.item.amount }}
                        <template v-slot:input>
                          <v-text-field
                            v-model="props.item.amount"
                            :rules="[max25chars]"
                            :label="frappe._('Edit')"
                            single-line
                            counter
                            type="number"
                           
                          ></v-text-field>
                        </template>
                      </v-edit-dialog>
                    </template>

                    <template v-slot:item.count="props">
                    <v-edit-dialog :return-value.sync="props.item.count">
                      {{ props.item.count }}
                      <template v-slot:input>
                        <v-text-field
                          v-model="props.item.count"
                          :rules="[max25chars]"
                          :label="frappe._('Edit')"
                          single-line
                          counter
                          type="number"
                          @change="change_update_amount($event,props.item)"
                        ></v-text-field>

                      </template>
                    </v-edit-dialog>
                  </template>
                  </v-data-table> -->
                  <v-simple-table>
                      <template v-slot:default>
                        <thead>
                          <tr>
                            <th class="text-center" width='100px'>
                              Currency
                            </th>
                            <th class="text-center" width='100px'>
                              Count
                            </th>
                            <th class="text-center" width='100px'>
                              Amount
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                          v-for="items in change_denomination_data"
                          :key="items.currency">
                            <td><v-text-field placeholder="Currency" v-model="items.currency" dense readonly></v-text-field></td>
                            <td><v-text-field placeholder="Count" v-model="items.count" dense @change="change_update_amount($event,items)"></v-text-field></td>
                            <td><v-text-field placeholder="Amount" v-model="items.amount" dense readonly></v-text-field></td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>
                </template>

              </v-col>

            </v-container>
        

          </v-row>
         
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="close_dialog">Close</v-btn>
            <v-btn color="success" dark @click="submit_dialog">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  
  <script>
  import { evntBus } from '../../bus';
  export default {
    // props: ["draftsDialog"],
    data: () => ({
      invoice:[],
      draftsDialog: false,
      singleSelect: true,
      grand_amount : 0,
      total_amount:0,
      diff_amount:0,
      change_total_amount:0,
      selected: [],
      currency : [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1],
      change_currency : [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1],
      dialog_data: {},
      denomination_headers:[
      {
        text: __('Currency'),
        align: 'start',
        sortable: false,
        value: 'currency',
      },
      {
        text: __('Count'),
        value: 'count',
        align: 'center',
        sortable: false,
        
      },
      {
        text: __('Amount'),
        value: 'amount',
        align: 'center',
        sortable: false,
      },
      ],
      change_footer:[
      {
        text: __('Currency'),
        align: 'start',
        sortable: false,
        value: 'currency',
      },
      {
        text: __('Count'),
        value: 'count',
        align: 'center',
        sortable: false,
        
      },
      {
        text: __('Amount'),
        value: 'amount',
        align: 'center',
        sortable: false,
      },
      ],

      denomination_data:[
   

      ],
      change_denomination_data:[
   

      ],
      
    }),
    
    watch: {},
    methods: {
      update_amount(value,row){
      row.amount = row.currency * row.count
      this.total_amount = 0
      this.actual_amt = 0
      this.denomination_data.forEach((data) =>{
        this.total_amount += data.amount
        this.diff_amount = this.total_amount - this.grand_amount
        this.actual_amt =  this.diff_amount
        
      })

    },
    change_update_amount(value,row){
      row.amount = row.currency * row.count
      this.change_total_amount = 0

      this.change_denomination_data.forEach((data) =>{
        this.change_total_amount += data.amount
        

      })
      this.diff_amount = this.change_total_amount - this.actual_amt


    },
      close_dialog() {
        this.draftsDialog = false;
      },
  
      submit_dialog() {
        frappe.call('posawesome.posawesome.api.posapp.sales_invocie_denomination', {
          sales_invoice_doc:this.invoice,
          denomination_data:this.denomination_data,
          change_denomination_data:this.change_denomination_data,
          
        })
        .then((r) => {
          if (!r.exe) {
            evntBus.$emit('update_invoice_doc_after_denomination', r.message)
            this.draftsDialog = false;
            this.change_denomination_data =[]
            this.denomination_data = []
            this.grand_amount = 0
            this.diff_amount = 0
            this.change_total_amount = 0
            this.currency.forEach((i) => {
        this.denomination_data.push(   {
        "currency":i,
        "count":0,
        "amount":0
      },)
    })
    this.change_currency.forEach((i) => {
        this.change_denomination_data.push(   {
        "currency":i,
        "count":0,
        "amount":0
      },)
    })

          }
        });
        // this.draftsDialog = false;

      },
    },
    created: function () {
      evntBus.$on('open_denomination', (data) => {
        this.grand_amount = data.grand_total
        this.invoice = data
    this.draftsDialog = true;
      });
      this.currency.forEach((i) => {
        this.denomination_data.push(   {
        "currency":i,
        "count":0,
        "amount":0
      },)
    })
    this.change_currency.forEach((i) => {
        this.change_denomination_data.push(   {
        "currency":i,
        "count":0,
        "amount":0
      },)
    })
    },
  };
  </script>
  