import React from 'react';
import './App.css';
import axios from 'axios';

function getAllWashTimes(){
    axios({
        url: 'http://127.0.0.1:8000/api/',
        method: 'POST',
        data: {
            query: `
            {
                residents {
                    roomNumber
                    washtimeSet {
                        startTime
                        endTime
                    }
                }
            }
            `
        },
    }).then((result) => {
        return result.data
    });
}

function App() {
    getAllWashTimes()
    .then(data => {
        return (
          <div className="App" class="m-4">
            {data}
          </div>
        );
    })
    .catch(err => console.log(err))
}


export default App;
