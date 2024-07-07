import React, { useState } from 'react';
import { Box, TextField, Button, List, ListItem, ListItemText, Typography } from '@mui/material';
import { runNode } from '../../services/api/layout';

const RunNode = ({ node }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        if (input.trim() !== '') {
            let msg;
            try {
                msg = JSON.parse(input);
            } catch (error) {
                console.error('Error parsing input:', error);
                msg = { data: input };
            }
            setMessages([...messages, { text: input, sender: 'user' }]);
            try {
                const response = await runNode(node.data, msg);
                setMessages(prevMessages => [...prevMessages, { text: JSON.stringify(response.data), sender: 'system' }]);
            } catch (error) {
                console.error('Error running node:', error);
                setMessages(prevMessages => [...prevMessages, { text: 'Error running node', sender: 'system' }]);
            }
            setInput('');
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '80%' }}>
            <List sx={{ flexGrow: 1, overflow: 'auto' }}>
                {messages.map((message, index) => (
                    <ListItem key={index} sx={{ justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start' }}>
                        <ListItemText 
                            primary={
                                <Typography component="span" style={{ whiteSpace: 'pre-line' }}>
                                    {message.text}
                                </Typography>
                            } 
                        />
                    </ListItem>
                ))}
            </List>
            <Box sx={{ display: 'flex', padding: 1, borderTop: '1px solid #ccc' }}>
                <TextField
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    fullWidth
                    placeholder="Type your message..."
                    variant="outlined"
                    sx={{ marginRight: 1 }}
                    multilinex1
                />
                <Button variant="contained" color="primary" onClick={handleSend}>
                    Send
                </Button>
            </Box>
        </Box>
    );
};

export default RunNode;
