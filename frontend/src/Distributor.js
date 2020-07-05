import React, { Component } from 'react';
import { API } from 'aws-amplify';

class Distributor extends Component {

    constructor(props) {
        super(props);
        this.state = {
            email: '',
            emailMessage: '',
            licenseCode: '',
            apiMessage: '',
            errMessage: ''
        };

    }

    distributeLicenseCode() {

        // 画面初期化
        this.initDisplay();

        let email = this.state.email;
        let error = false;

        if (email == null || email === "") {
            this.setState({
                emailMessage: "メールアドレスを入力してください。"
            });
            error = true;
        }

        if (error) {
            return;
        }

        // Task: API Call
        console.log("Call LicenseCodeDistributor API");
        let apiName = 'LicenseCodeDistributorAPI';
        let path = `/license-codes`;
        let postData = {
            headers: {},
            body: {
                "email": email
            },
            response: true
        };
        API.post(apiName, path, postData).then(response => {
                var result = response.data;
//                console.log("API call Post is succeeded!", result);
                this.setState({
                    course: result.course,
                    licenseCode: result.licenseCode,
                    apiMessage: result.message
                });
            })
            .catch(err => {
                this.setState({
                    errMessage: "エラーが発生しました。"
                })
                console.log("api call error: ", err);
            });
    }
    initDisplay() {
        this.setState({
            course: '',
            emailMessage: '',
            licenseCode: '',
            apiMessage: '',
            errMessage: ''
        });
    }

    render() {

        return (
            <div className="control-group">
              <h3>【AWS Training】 テキストのライセンスコード取得</h3><br/>
              <h4>トレーニング申込時のメールアドレスを入力し、取得ボタンを押してください</h4>
              <br />
              <div/>
              <div className="control-group">
                <label className="control-label">メールアドレス:　</label>
                    <input type="text" name="email" value={this.state.email}
                       onChange={(e) => this.setState({email: e.target.value})}
                       style={{width: "80%"}}/>
                <div style={{color: "red"}}>
                    {this.state.emailMessage}
                </div>
              </div>
            <br></br>

              <div className="control-group">
                <div className="controls">
                      <input className="btn btn-primary" type="button" id="getlicense_btn" value="取得" onClick={() => this.distributeLicenseCode()} />
                </div>
              </div>
              <br></br>
              <div style={{color: "red"}}>
                {this.state.apiMessage}
              </div>
            {
              this.state.licenseCode ?

                  <div>
                    <h3>
                    ライセンスコードは、{this.state.licenseCode} です。
                    </h3>
                  </div>
              :
                <div/>
              
            
            }
              <div style={{color: "red"}}>
                {this.state.errMessage}
              </div>
            </div>
        );
    }
}


export default Distributor;
