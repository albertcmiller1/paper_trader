import React, {useState} from "react";
import { Form, Row, Col, FormGroup, Input, Label, Button, DropdownItem } from 'reactstrap';

const HomePage = () => {
    const [selectedItem, setSelectedItem] = useState(null);
    const [ticker, setTicker] = useState(null);
    const [price, setPrice] = useState(null);
    const [quantity, setQuantity] = useState(null);
    const items = ["Bid", "Ask"];

    const placeOrder = () => {
        console.log(selectedItem)
        console.log(ticker)
        console.log(price)
        console.log(quantity)
    }

    return (
        <div>
            <center>
            <h1>
                Paper Trader | Trade
            </h1>
            </center>
            <Form>
                <Row> 
                    <Col></Col>
                    <Col>
                        <FormGroup>
                                <Label>
                                Ticker
                                </Label>
                                <Input
                                placeholder="AAPL"
                                onInput={e => setTicker(e.target.value)}
                                />
                            </FormGroup>
                    </Col>
                    <Col>
                        <FormGroup>
                            <Label>
                            Limit Price
                            </Label>
                            <Input
                            placeholder="100.00"
                            onInput={e => setPrice(e.target.value)}
                            />
                        </FormGroup>
                    </Col>
                    <Col> 
                        <FormGroup>
                                <Label>
                                Quantity
                                </Label>
                                <Input
                                placeholder="1"
                                onInput={e => setQuantity(e.target.value)}
                                />
                        </FormGroup>  
                    </Col>
                    <Col>
                        <FormGroup tag="fieldset">
                            <legend>Trade Type</legend>
                            <FormGroup check onClick={() => setSelectedItem("Bid")}>
                                <Input
                                    name="radio1"
                                    type="radio"
                                    />
                                <Label check >Bid</Label>
                            </FormGroup>
                            <FormGroup check onClick={() => setSelectedItem("Ask")}>
                                <Input
                                    name="radio1"
                                    type="radio"
                                    />
                                <Label check>Ask</Label>
                            </FormGroup>
                        </FormGroup>
                    </Col>
                    <Col>
                        <Button onClick={placeOrder} outline color="success">Place Order</Button>
                    </Col>
                    <Col></Col>
                </Row>
            </Form>
        </div>
    );
};

export default HomePage;