<template>
    <v-row justify="center">
      <v-dialog v-model="closingDialog" max-width="900px">
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Closing POS Shift')
            }}</span>
          </v-card-title>
          <v-card-text class="pa-0">
            <v-container>
              <v-row>
                <v-col cols="6" class="pa-1">
                  <template>
                    <v-data-table
                      :headers="headers"
                      :items="dialog_data.payment_reconciliation"
                      item-key="mode_of_payment"
                      class="elevation-1"
                      :items-per-page="itemsPerPage"
                      hide-default-footer
                    >
                      <template v-slot:item.closing_amount="props">
                        <v-edit-dialog
                          :return-value.sync="props.item.closing_amount"
                        >
                          {{ formtCurrency(props.item.closing_amount) }}
                          <template v-slot:input>
                            <v-text-field
                              v-model="props.item.closing_amount"
                              :rules="[max25chars]"
                              :label="frappe._('Edit')"
                              single-line
                              counter
                              type="number"
                            ></v-text-field>
                          </template>
                        </v-edit-dialog>
                      </template>
                      <template v-slot:item.difference="{ item }">{{
                        (item.difference = formtCurrency(
                          item.expected_amount - item.closing_amount
                        ))
                        
                      }}</template>
                      <template v-slot:item.opening_amount="{ item }">
                        
                      {{
                        formtCurrency(item.opening_amount)
                        
                      }}</template>
                      
                      <template v-slot:item.expected_amount="{ item }">{{
                        formtCurrency(item.expected_amount)
                      }}</template>
                    </v-data-table>
                  </template>
                </v-col>
                <v-col cols="6" class="pa-1">
                  <template>
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
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="close_dialog">{{
              __('Close')
            }}</v-btn>
            <v-btn color="success" dark @click="submit_dialog">{{
              __('Submit')
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  
  <script>
  import { evntBus } from '../../bus';
  export default {
    data: () => ({
      closingDialog: false,
      itemsPerPage: 20,
      dialog_data: {},
      pos_profile: '',
      currency : [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1],
      headers: [
        {
          text: __('Mode of Payment'),
          value: 'mode_of_payment',
          align: 'start',
          sortable: true,
        },
        {
          text: __('Opening Amount'),
          align: 'end',
          sortable: true,
          value: 'opening_amount',
        },
        {
          text: __('Closing Amount'),
          value: 'closing_amount',
          align: 'end',
          sortable: true,
        },
      ],
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
        opening_denomination : [],
        denomination_data:[],
      max25chars: (v) => v.length <= 20 || 'Input too long!', // TODO : should validate as number
      pagination: {},
    }),
    watch: {},
    methods: {
      update_amount(value,row){
        row.amount = row.currency * row.count
        let total_amount = 0
        this.denomination_data.forEach((data) =>{
          total_amount += data.amount
        })
        this.payments_methods.forEach((m)=>{
          if (m.is_cash){
            m.amount = total_amount
          }
        })
      },
      close_dialog() {
        this.closingDialog = false;
      },
  
      submit_dialog() {
        this.dialog_data.denomination_table = this.denomination_data //#core code
        evntBus.$emit('submit_closing_pos', this.dialog_data);
        this.closingDialog = false;
      },
      formtCurrency(value) {
        value = parseFloat(value);
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
    },
    created: function () {
      evntBus.$on('open_ClosingDialog', (data) => {
        this.closingDialog = true;
        this.dialog_data = data;
        this.denomination_data =[]
        frappe.db.get_doc('POS Opening Shift', this.dialog_data.pos_opening_shift).then((doc) => {
          doc.denomination_table.forEach((i) => {
          this.denomination_data.push(   {
              "currency":i.currency,
              "count":i.count,
              "amount":i.amount
            },)
          })
              });
      });
      
      
      evntBus.$on('register_pos_profile', (data) => {
        this.pos_profile = data.pos_profile;
        if (!this.pos_profile.hide_expected_amount) {
          this.headers.push({
            text: __('Expected Amount'),
            value: 'expected_amount',
            align: 'end',
            sortable: false,
          });
          this.headers.push({
            text: __('Difference'),
            value: 'difference',
            align: 'end',
            sortable: false,
          });
        }
      });
  
    },
  };
  </script>
  