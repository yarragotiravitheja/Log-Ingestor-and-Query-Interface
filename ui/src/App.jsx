import React, { useEffect, useState } from 'react'
import { QueryBuilder, formatQuery, defaultValidator, ValueSelector } from 'react-querybuilder';
import './App.css'
import 'react-querybuilder/dist/query-builder.scss';
import { defaultOperators } from 'react-querybuilder';


const API_URL = "http://localhost:3000"

const initialQuery = {
  combinator: 'and', rules: [
    {
      "field": "level",
      "value": ""
    }
  ]
};

const validator = (r) => !!r.value;

const getDateTimeLocalFormat = () => {
  const today = new Date();
  return today.toISOString().slice(0, 11)
}

const equalsOperator = defaultOperators.filter((op) => op.name === "=")
const betweenOperator = defaultOperators.filter((op) => op.name === "between")
const containsOperator = defaultOperators.filter((op) => op.name === "contains")


function App() {
  const [query, setQuery] = useState(initialQuery);
  const [levelOptions, setLevelOptions] = useState(null);
  const [resourceOptions, setResourceOptions] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [enquedJobs, setEnquedJobs] = useState(0);

  const fields = [
    {
      name: 'level',
      label: 'level',
      valueEditorType: 'select',
      values: levelOptions,
      operators: equalsOperator,
    },
    {
      name: 'resource',
      label: 'resourceId',
      valueEditorType: 'select',
      values: resourceOptions,
      operators: equalsOperator,
    },
    {
      name: "message",
      label: "message",
      placeholder: 'Filter logs by message',
      operators: containsOperator
    },
    {
      name: 'timestamp',
      label: 'timestamp',
      inputType: 'datetime-local',
      operators: betweenOperator,
      defaultValue: `${getDateTimeLocalFormat() + '00:00'},${getDateTimeLocalFormat() + '23:59'}`,
      validator
    },
    {
      name: "traceId",
      label: "traceId",
      placeholder: 'Filter logs by traceId',
      operators: equalsOperator,
    },
    {
      name: "spanId",
      label: "spanId",
      placeholder: 'Filter logs by spanId',
      operators: equalsOperator,
    },
    {
      name: "commit",
      label: "commit",
      placeholder: 'Filter logs by commit hash',
      operators: equalsOperator,
    },
    {
      name: "parentResourceId",
      label: "parentResourceId",
      placeholder: 'Filter logs by parentResourceId',
      operators: equalsOperator,
    },
  ]

  const getLogIngestionInfo = () => {
    fetch(`${API_URL}/django-rq/stats.json/test/`).then((data) => data.json()).then((d) => {
      setEnquedJobs(d.queues[0].jobs)
    })

  }

  useEffect(() => {
    // API call to get values for log levels and resource ids for selection
    fetch(`${API_URL}/init_filter`).then((data) => data.json()).then((d) => {
      let levels = d.levels;
      let resources = d.resources;

      levels = levels.map((level) => ({ name: level.level, label: level.level }))
      resources = resources.map((resource) => ({ name: resource.resource, label: resource.resource }))

      levels.unshift({ name: "", value: "" })
      setLevelOptions(levels)
      setResourceOptions(resources)
    })

    // API call to get the log ingestion queue stats
    getLogIngestionInfo();
    const timer = setInterval(() => {
      getLogIngestionInfo()
    }, 4000);

    return () => clearInterval(timer);
  }, [])


  const resetPage = () => {
    setLogs([]);
    setCurrentPage(1);
  }


  const fetchLogs = (pageNum) => {
    let jsonQuery = formatQuery(query)
    jsonQuery = JSON.parse(jsonQuery)
    jsonQuery.page = pageNum
    jsonQuery.rules[0].value = jsonQuery.rules[0].value.trim()
    setLoading(true)
    setError(false)
    fetch(`${API_URL}/fetch_logs`, {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(jsonQuery)
    }).
      then((data) => data.json()).
      then((logs) => {
        setLogs(logs)
        setCurrentPage(pageNum)
        window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
        setLoading(false)
        setError(false)
      }).catch((err) => {
        setLoading(false)
        setError(true)
      })
  }


  if (!levelOptions || !resourceOptions) {
    return <h1>Loading</h1>
  }
  const CustomFieldSelector = (props) => {
    const fieldChanged = (param) => {
      props.handleOnChange(param)
      resetPage()
    }
    return <ValueSelector {...props} handleOnChange={fieldChanged}></ValueSelector>
  }

  const LogList = ({ logs }) => {

    if (logs.length === 0 && !error) {
      return <h2>Nothing to show...</h2>
    }

    if (error) {
      return <h2>Something went wrong !!!</h2>
    }

    return (
      <>
        <p>Page: {currentPage}</p>
        <div style={{
          marginBottom: "60px"
        }}>
          {
            logs.map((log, idx) => {
              return (<pre key={idx} style={{
                whiteSpace: "pre-wrap",
                padding: "4px",
                borderRadius: "8px",
                background: "#f1f1f1",
              }}>{JSON.stringify(log)}</pre>)
            })
          }</div>
      </>)
  }

  return (
    <div style={{
      width: "60%"
    }}>
      <h1 style={{textAlign: "center"}}>Log Querying</h1>
      <QueryBuilder
        fields={fields}
        query={query}
        onQueryChange={setQuery}
        validator={defaultValidator}
        controlElements={{ fieldSelector: CustomFieldSelector }}
      />
      <button onClick={() => fetchLogs(1)} disabled={loading} style={{ marginLeft: "auto" }} className='app-button'>Fetch Logs</button>
      {enquedJobs > 0 ? <p>Workers are ingesting {enquedJobs} logs</p> : null}
      {
        loading ? <h2>Loading</h2> : <LogList logs={logs} />
      }
      <div className='pagination-container'>
        <div className='pagination-button-container'>
          <button className='app-button button-shadow' disabled={currentPage === 1} onClick={() => fetchLogs(currentPage - 1)}>{"<"}</button>
          <button className='app-button button-shadow' disabled={logs.length === 0} onClick={() => fetchLogs(currentPage + 1)}>{">"}</button>
        </div>
      </div>
    </div>
  )
}

export default App